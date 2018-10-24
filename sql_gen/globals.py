from sql_gen.emproject import current_emproject#,addb
import pymssql
import sys

def camelcase(st):
    output = ''.join(x for x in st.title() if x.isalnum())
    return output[0].lower() + output[1:]

def prj_prefix():
    return EMProject.prefix()

def adquery(query):
    return addb.query(query)
