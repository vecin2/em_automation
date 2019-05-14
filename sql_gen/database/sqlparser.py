import re
import sqlparse

storage_table = {
                 "CC": {"Home": 100},
                 "ENV":{"Dflt": 666},
                 "RELEASE":{"ID":1},
                 "ET":{"Agent":602}
                }

class NonConflictRelativeIdLoader(object):
    def __init__(self,db=None):
        self.db =db
    def load(self,keyset,keyname):
        query ="SELECT ID FROM CCADMIN_IDMAP where keyset = '{}' AND KEYNAME ='{}'"
        try:
            result =self.db.find(query.format(keyset,keyname))
            return result["ID"]
        except LookupError as excinfo:
            return self.generate_id(keyset,keyname)
    def generate_id(self,keyset,keyname):
        query ="SELECT ID FROM CCADMIN_IDMAP where keyset ='{}' order by id"
        result =self.db.list(query.format(keyset))[0]
        if result >0:
            return -1
        else:
            result -=1
            return result

class RelativeIdLoader(object):
    def __init__(self,db=None):
        self.db =db
    def load(self,keyset,keyname):
        query ="SELECT ID FROM CCADMIN_IDMAP where keyset = '{}' AND KEYNAME ='{}'"
        try:
            result =self.db.find(query.format(keyset,keyname))
            return result["ID"]
        except LookupError as excinfo:
            return self.generate_id(keyset,keyname)

    def generate_id(self,keyset,keyname):
        query ="SELECT ID FROM CCADMIN_IDMAP where keyset ='{}' order by id desc"
        result =self.db.list(query.format(keyset))
        if result:
            max_id = result[0]
            generated_id = max_id +1
            insert_id_query="INSERT INTO CCADMIN_IDMAP (KEYSET,KEYNAME,ID) "+\
                            "VALUES ('"+keyset+"','"+keyname+"','"+str(generated_id)+"');"
            self.db.execute(insert_id_query)
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
            classic_syntax = self.convert_set_clause(set_clause)
            return query.replace(set_clause,classic_syntax)
        return query

    def extract_set_group(self,s):
        return self.get_text_in_between(s,"SET","WHERE")

    def convert_set_clause(self,string):
        before_equals=string.split("=")[0]
        after_equals=string.split("=")[1]
        column_names = self.get_text_in_between(before_equals,"(",")").split(",")
        values = self.get_text_in_between(after_equals,"(",")").split(",")
        return self.equalize_items_str(column_names,values)

    def equalize_items_str(self,list1,list2):
        result=""
        for index, column_name in enumerate(list1):
            if result:
                result +=", "
            result += column_name+"="+list2[index]
        return result

    def get_text_in_between(self,s,start,end):
        where_index =s.upper().rfind(end)
        if where_index <0:
            where_index =len(s)
        set_index =s.upper().find(start)
        return s[set_index+len(start):where_index].strip()

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

    def parse_runnable_statements(self,sqltext):
        #sqltext = self.parse_relative_ids(sqltext)
        #sqltext = self.strip_comments(sqltext)
        #sqltext = self.parse_update_stmt(sqltext)
        statements = self.split(sqltext)
        result =[]
        for stmt in statements:
            result.append(self.parse_runnable_stament(stmt))
        return result

    def parse_runnable_stament(self,statement):
            statement = self.parse_relative_ids(statement)
            statement = self.strip_comments(statement)
            return self.parse_update_stmt(statement)

    def parse_assertable_statements(self,sqltext):
        sqltext = self.strip_comments(sqltext)
        sqltext = sqltext.replace(" ","")
        sqltext = sqltext.replace("\t","")
        sqltext = sqltext.replace("\r","")
        sqltext = sqltext.replace("\n","")
        return self.split(sqltext)
