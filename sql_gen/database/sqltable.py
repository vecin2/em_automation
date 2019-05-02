import sql_gen
from prettytable import PrettyTable

class SQLTable(object):
    def __init__(self, rows_dict=None):
        if rows_dict:
            self.rows =rows_dict
        else:
            self.rows=[]

    def __getitem__(self, arg):
        return self.rows[arg]

    def __len__(self):
        return len(self.rows)

    def __iter__(self):
        return self.rows.__iter__()

    def __repr__(self):
        prettytable = PrettyTable()
        if self.rows:
            prettytable.field_names = self.rows[0]._headers()
        for row in self.rows:
            prettytable.add_row(list(row.values()))
        return str(prettytable)

    def append(self, row):
        self.rows.append(row)

    def clone(self):
        return SQLTable(self.rows.copy())

    def where(self,*args,**kwargs):
        result =self.clone()
        filters =self._get_filters(*args,**kwargs)
        for sqlfilter in filters:
           result =sqlfilter.apply(result)
        return result

    def _get_filters(self,*args,**kwargs):
        filters = self._get_keyvalue_filters(**kwargs)
        #filters.extend(self._get_expr_filters(args))
        return filters

    def _get_keyvalue_filters(self,**kwargs):
        filters=[]
        for key in kwargs:
            upper_key = key.upper()
            value =kwargs[key]
            filters.append(KeyValueFilter(key.upper(),value))
        return filters

    def _get_expr_filters(self,*args):
        filters=[]
        for expr in args:
            upper_key = key.upper()
            value =kwargs[key]
            filters.append(KeyValueFilter(key.upper(),value))
        return filters


class SQLRow(dict):
    def __init(self, dict_row):
        dict.__init__(self,dict_row)

    def __getitem__(self,key):
        if dict.__getitem__(self,key) is None:
            return "NULL"
        return dict.__getitem__(self,key)

    def __repr__(self):
        prettytable = PrettyTable()
        prettytable.field_names = self._headers()
        prettytable.add_row(list(self.values()))
        return str(prettytable)

    def _headers(self):
        return list(self.keys())


class KeyValueFilter(object):
    def __init__(self,key,value):
        self.key =key
        self.value =value

    def apply(self,table):
        result = SQLTable()
        for row in table:
            if self.is_valid(row):
                result.append(row)
        return result

    def is_valid(self,row):
        return self.key in row\
                    and Matcher.match(row[self.key],self.value)

class Matcher(object):
    @staticmethod
    def match(value1, value2):
        type1 = type(value1)
        sql_gen.logger.info("Matching '"+ str(value1) + "' of  type '"+str(type1)+"'"+\
                              "with '"+str(value2)+"' of type '"+str(type(value2))+"'.")
        value2_cast =type1(value2)
        result = value1 == value2_cast
        if result:
            sql_gen.logger.info("They match!")
        else:
            sql_gen.logger.info("They dont match")
        return result



