import pytest


#def test_some():
#    _addb.list.idmap_keynames__by_id("ED")
#
#    verb_name = _addb.fetch.v_names__by_ed_id(entity_def_id)
#    verb_name = _addb.list(v__by_ed_id(entity_def_id),"NAME")
#
#    _addb.find.pd__by_ed_id_and_verb_name(entity_def_id, verb_name)
#        _col(name).of(_addb.fetch(v__by_id.using(entity_def_id)))

queries ={"v__by_name":"SELECT * FROM verb_name WHERE NAME='{}' and IS_DELETED='{}'"}
class AttrDict(object):
    def __init__(self,dict):
        self.dict = dict
    def __getattr__(self, item):
        return self.dict[item]

    def __dir__(self):
        return super().__dir__() + [str(k) for k in self.keys()]

class StringFormat:
    def __init__(self,string):
       self.string = string

    def __call__(self,*args):
        return self.string.format(*args)

class ADDB(object):
    class Fetch(AttrDict):
        def __getattr__(self, item):
            return StringFormat(super().__getattr__(item))


    fetch = Fetch(queries)

def test_fetch():
    addb = ADDB()
    query_formatted = "SELECT * FROM verb_name WHERE NAME='inlineSearch' and IS_DELETED='N'"
    assert query_formatted==addb.fetch.v__by_name("inlineSearch",'N')

#def test_fetch_real(fs):
    #queries_content ="v_by_name=SELECT * FROM verb_name WHERE NAME={}"
    #queries_file = "create_file"
    #addb = EMProject.getADDB()
    #addb.fetch.v__by_ed_id("Customer")
