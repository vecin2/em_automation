
This template shows the different APIs to query database

**1. USING '_db'**
The db class allows to fetch the agent desktop db from a predefined set of queries defined in the "queries.sql" file.

It has three main operations: find, list and fetch
{% set verb_id = tmp_pd_config | description("verb_id") | default("2129") %}
*_db.find*
It returns one row as dictionary. If more that one row is found it throws an exception. For example:
	{{ '{%' }} set find_verb= _db.find.v__by_id(verb_id) {{ '%}' }} 
	{% set find_verb= _db.find.v__by_id(verb_id) %}

Returns:
	find_verb['NAME']={{find_verb['NAME']}}
	find_verb['ID']={{find_verb['ID']}}

*_db.list*
It returns the first column of items as a list. For example:
	{{ '{%' }} set verb_list= _db.list.v_names_by_ed("Customer") {{ '%}' }} 
	{% set verb_list= _db.list.v_names_by_ed("Customer") %}

Returns:
	verb_list[0]={{verb_list[0]}}
	verb_list[1]={{verb_list[1]}}

*_db.fetch*
It returns a list of dictionaries. For example:
	{{ '{%' }} set fetch_verb= _db.fetch.v__by_id(verb_id) {{ '%}' }}
       	{% set fetch_verb= _db.fetch.v__by_id(verb_id) %}

Returns:
	fetch_verb[0]['NAME']={{fetch_verb[0]['NAME']}}


**2. USING '_database'**
_database allows to fetch the agent desktop db passing hardcoded SQL

It has the same three main operations: find, list and fetch

*_database.find*
Example:
	{{ '{%' }} set find_verb= _database.find("SELECT * FROM eva_verb where id= 2129") {{ '%}' }}
	{% set find_verb= _database.find("SELECT * FROM eva_verb where id= 2129") %}
Returns:
	find_verb['NAME']={{find_verb['NAME']}}

*_database.list*
Example:
	{{ '{%' }} set verb_list= _database.list("SELECT NAME eva_verb where id= 2129") {{ '%}' }}
	{% set verb_list= _database.list("SELECT NAME, ID FROM eva_verb where name like '%search%'") %}
Returns:
	verb_list[0]={{verb_list[0]}}
	verb_list[1]={{verb_list[1]}}

*_database.fetch*
Example:
	{{ '{%' }} set verb_fetch= _database.fetch("SELECT NAME eva_verb where id= 2129") {{ '%}' }}
	{% set verb_fetch= _database.fetch("SELECT NAME, ID FROM eva_verb where name like '%search%'") %}
Returns:
	verb_fetch[0]['NAME'] ={{verb_fetch[0]['NAME']}}
	verb_fetch[0]['ID'] ={{verb_fetch[0]['ID']}}
	verb_fetch[1]['NAME'] ={{verb_fetch[1]['NAME']}}
	verb_fetch[1]['ID'] ={{verb_fetch[1]['ID']}}

**3. USING '_Query'**
It allows to retrieve all the queries within 'queries.sql' so  they can pass to the database object

For example:
	{{ '{%' }} set find_verb= _database.find(_Query.v__by_id(verb_id)) {{ '%}' }} 
{% set find_verb= _database.find(_Query.v__by_id(verb_id)) %}
Returns:
	find_verb['NAME']={{find_verb['NAME']}}
