
USED PREDEFINED QUERIES
Running find returns a dictionary with column names as keys.
For example:
	{{ '{%' }} set fin_verb= _db.find.v__by_id(verb_id | default("2129")) {{ '%}' }} {% set find_verb= _db.find.v__by_id(verb_id | default("2129")) %}
Returns find_verb['NAME']={{find_verb['NAME']}}

Running fetch returns a list of dictionaries.
For example:
	{{ '{%' }} set fetch_verb= _db.fetch.v__by_id(verb_id | default("2129")) {{ '%}' }} {% set fetch_verb= _db.fetch.v__by_id("2129") %}

Returns fetch_verb[0]['NAME']={{fetch_verb[0]['NAME']}}

Running list returns the first column as a list
For example:
	{{ '{%' }} set verb_list= _db.list.v_names_by_ed("Customer") {{ '%}' }} {% set verb_list= _db.list.v_names_by_ed("Customer") %}

Returns verb_list[0]={{verb_list[0]}}
Returns verb_list[1]={{verb_list[1]}}


USING DATABASE object
Find can be achieved with "_database" object as well
For example:
	{{ '{%' }} set find_verb= _database.find(Queries.v__by_id(verb_id | default("2129")) {{ '%}' }} 
{% set find_verb= _database.find("SELECT * FROM eva_verb where id= 2129") %}
Returns find_verb['NAME']={{find_verb['NAME']}}

Find can be achieved with "_database" object as well
For example:
	{{ '{%' }} set find_verb= _database.find(Queries.v__by_id(verb_id | default("2129")) {{ '%}' }} 
{% set find_verb= _database.find(_Query.v__by_id("2129")) %}
Returns find_verb['NAME']={{find_verb['NAME']}}
