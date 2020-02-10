import re
from collections import defaultdict
import sqlparse

storage_table = {
                 "CC": {"Home": 100},
                 "ENV":{"Dflt": 666},
                 "RELEASE":{"ID":1},
                 "ET":{"Agent":602}
                }

class RelativeIdLoader(object):
    keynames_cache={}
    #cache to avoid generating id multiple times
    keyset_cache=defaultdict(list)
    def __init__(self,db=None):
        self.db =db
    def load(self,keyset,keyname):
        id = self._get_from_cache(keyset,keyname)
        if id:
            return id
        else:
            result = self.compute_id(keyset,keyname)
            self._cache_keyname(keyset,keyname,result)
            return result

    def list(self,keyset):
        result =  self._list_from_cache(keyset)
        if result:
            return result
        else:
            result = self._fetch_keyset(keyset)
            return result
    @staticmethod
    def clearcache():
        RelativeIdLoader.keyset_cache.clear()
        RelativeIdLoader.keynames_cache.clear()

    def full_keyname_by_id(self,keyset,id):
        if id == "NULL":
            return id
        return "@"+keyset+"."+self.keyname_by_id(keyset,id)

    def keyname_by_id(self,keyset,id):
        return self.db.find("SELECT KEYNAME FROM CCADMIN_IDMAP WHERE KEYSET ='"+keyset+"' AND ID ="+str(id))["KEYNAME"]


    def _fetch_keyset(self,keyset):
        result = self.db.fetch("SELECT KEYNAME,ID FROM CCADMIN_IDMAP WHERE KEYSET ='"+keyset+"'")
        self._cache_keyset(keyset,result)
        return result.column("KEYNAME")

    def _cache_keyset(self,keyset,result):
        for record in result:
            self._cache_keyname(keyset,record["KEYNAME"],record["ID"])

    def _list_from_cache(self,keyset):
        if keyset in RelativeIdLoader.keyset_cache:
            return RelativeIdLoader.keyset_cache[keyset]

    def _cache_keyname(self,keyset,keyname,value):
        key=keyset+"."+keyname
        if key not in RelativeIdLoader.keynames_cache:
            RelativeIdLoader.keynames_cache[key]=value
            RelativeIdLoader.keyset_cache[keyset].append(keyname)

    def _get_from_cache(self,keyset,keyname):
        key=keyset+"."+keyname
        if key in RelativeIdLoader.keynames_cache:
            return RelativeIdLoader.keynames_cache[key]
        return None

    def compute_id(self,keyset,keyname):
            query ="SELECT ID FROM CCADMIN_IDMAP where keyset = '{}' AND KEYNAME ='{}'"
            result =self.db.fetch(query.format(keyset,keyname))
            if len(result) == 1:
                return result[0]["ID"]
            elif len(result) == 0:
                return self.generate_id(keyset,keyname)
            else:
                return self._handle_duplicate_keys(keyset,keyname,result[0]["ID"])

    def _handle_duplicate_keys(self,keyset,keyname,id):
            query ="delete from CCADMIN_IDMAP where keyset ='{}' and keyname='{}'"
            result =self.db.execute(query.format(keyset,keyname))
            query ="INSERT INTO CCADMIN_IDMAP (KEYSET,KEYNAME,ID) VALUES ('{}','{}',{});"
            result =self.db.execute(query.format(keyset,keyname,id))
            error_msg="Found multiple records for keyset '"+keyset+"'"+\
                        " and keyname '"+keyname+"' combination. There should"+\
                        " be only one record or none if this is a new entity.\n  {} extra ids where removed"
            print(error_msg.format(result.rowcount))
            return id

    def generate_id(self,keyset,keyname):
        query ="SELECT ID FROM CCADMIN_IDMAP where keyset ='{}' order by id desc".format(keyset)
        result =self.db.list(query)
        if result:
            max_id = result[0]
            generated_id = max_id +1
            insert_id_query="INSERT INTO CCADMIN_IDMAP (KEYSET,KEYNAME,ID) "+\
                            "VALUES ('"+keyset+"','"+keyname+"','"+str(generated_id)+"');"
            self.db.execute(insert_id_query)
            self.db.clear_cache_item(query)
            return generated_id


class RelativeId(object):
    relativeid_exp="(?<=[^\w])@\w*\.\w*"
    def __init__(self,string,loader=None):
        self.string = string
        self.loader =loader

    @property
    def keyset(self):
        return self.string.split(".")[0][1:]

    @property
    def keyname(self):
        return self.string.split(".")[1]

    def real_id(self):
        return str(self.loader.load(self.keyset,self.keyname))

    def replace_all_instances(self,sqltext):
        return sqltext.replace(self.string,self.real_id())


class RelativeIdReplacer(object):
    def __init__(self,loader=None):
        self.loader = loader
    REG_EXP="(?<=[^\w])@\w*\.\w*"
    def find_all(self,sqltext):
        #matches pattern @ET.inlineSearch
        ids =re.findall(self.REG_EXP,sqltext)
        #remove duplicates
        return list(set(ids))

    def replace(self,sqltext):
        relative_ids = self.find_all(sqltext)
        for str_relative_id in relative_ids:
            relative_id = RelativeId(str_relative_id,loader=self.loader)
            sqltext = relative_id.replace_all_instances(sqltext)
        return sqltext

class SQLParser(object):
    def __init__(self,loader=RelativeIdLoader()):
        self.relativeId_replacer = RelativeIdReplacer(loader)

    def strip_comments(self,sqltext):
        return sqlparse.format(sqltext,strip_comments=True).strip()

    def parse_update_stmt(self,query):
        first_word= query.split(" ")[0]
        if first_word.upper() == "UPDATE":
            set_clause =self.extract_set_group(query)
            if self.is_em_syntax(set_clause):
                classic_syntax = self.convert_set_clause(set_clause)
                return query.replace(set_clause,classic_syntax)
        return query

    def extract_set_group(self,s):
        return self.get_text_in_between(s,"SET","WHERE")

    def is_em_syntax(self,string):
        no_spaces_str =string.replace(" ","")
        matches = re.findall('\(.*\)=\(.*\)',no_spaces_str)
        if len(matches) ==1 and matches[0] ==no_spaces_str:
            return True
        return False

    def convert_set_clause(self,string):
        before_equals=string.split("=")[0]
        after_equals=string.split("=")[1]
        column_names = self.get_text_in_between(before_equals,"(",")").split(",")
        values = self.get_text_in_between(after_equals,"(",")").split(",")
        if column_names and values:
            return self.equalize_items_str(column_names,values)
        return string

    def equalize_items_str(self,list1,list2):
        result=""
        for index, column_name in enumerate(list1):
            if result:
                result +=", "
            result += column_name+"="+list2[index]
        return result

    def get_text_in_between(self,s,start,end):
        end_index =s.upper().rfind(end)
        if end_index <0:
            end_index =len(s)
        start_index =s.upper().find(start)
        text_in_btw = s[start_index+len(start):end_index].strip()
        if s == text_in_btw:
            return ""
        return text_in_btw


    def split(self,sqltext):
        result =[]
        for statement in sqlparse.split(sqltext):
            #remove semicolon - otherwise throws exc when run
            if statement :
                if statement[-1:]==";":
                    statement = statement[:-1]
                result.append(statement)
        return result

    def parse_relative_ids(self,sqltext):
        return self.relativeId_replacer.replace(sqltext)

    def parse_statements(self,sqltext):
        sqltext = self.strip_comments(sqltext)
        return self.split(sqltext)

    def parse_runnable_statements(self,sqltext):
        statements = self.parse_statements(sqltext)
        result =[]
        for stmt in statements:
            result.append(self.parse_runnable_stament(stmt))
        return result

    def parse_runnable_stament(self,statement):
            statement = self.parse_relative_ids(statement)
            return self.parse_update_stmt(statement)

    def parse_assertable_statements(self,sqltext):
        sqltext = self.strip_comments(sqltext)
        sqltext = sqltext.replace(" ","")
        sqltext = sqltext.replace("\t","")
        sqltext = sqltext.replace("\r","")
        sqltext = sqltext.replace("\n","")
        return self.split(sqltext)
