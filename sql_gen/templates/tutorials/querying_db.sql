
This template shows the different APIs to query database

**1. USING '_db'**
The db class allows to fetch the agent desktop db from a predefined set of queries defined in the "queries.sql" file.

It has three main operations: find, list and fetch
*_db.find*
It returns one row as dictionary. If more that one row is found it throws an exception. For example:
	{{ '{%' }} set find_ed= _db.find.ed_by_keyname('customer') {{ '%}' }} 
	{% set find_ed= _db.find.ed_by_keyname('Customer') %}

Returns:
	find_ed['NAME']={{find_ed['NAME']}}
	find_ed['ID']={{find_ed['ID']}}

*_db.fetch*
It returns a SQLTable which is a list of dictionaries with some additional methods. For example:
	{{ '{%' }} set fetch_verb= _db.fetch.v_by_pers_keyname(Home) {{ '%}' }}
       	{% set fetch_verb= _db.fetch.v_by_pers_keyname("Home") %}

Returns:
	fetch_verb[0]['DISPLAY_NAME']={{fetch_verb[0]['DISPLAY_NAME']}}

And you can access a column like this:
	fetch_verb.column('DISPLAY_NAME') == {{ fetch_verb.column('DISPLAY_NAME') }}

**2. USING '_database'**
_database allows to fetch the agent desktop db passing hardcoded SQL

It has the same three main operations: find, list and fetch

*_database.find*
Example:
	{{ '{%' }} set find_verb= _database.find("SELECT * FROM eva_verb where id= 2129") {{ '%}' }}
	{% set find_verb= _database.find("SELECT * FROM eva_verb where id= 2129") %}
Returns:
	find_verb['NAME']={{find_verb['NAME']}}

*_database.fetch*
Example:
	{{ '{%' }} set verb_fetch= _database.fetch("SELECT NAME eva_verb where id= 2129") {{ '%}' }}
	{% set verb_fetch= _database.fetch("SELECT NAME, ID FROM eva_verb where name like '%search%'") %}
Returns:
	verb_fetch[0]['NAME'] ={{verb_fetch[0]['NAME']}}
	verb_fetch[0]['ID'] ={{verb_fetch[0]['ID']}}
	verb_fetch[1]['NAME'] ={{verb_fetch[1]['NAME']}}
	verb_fetch[1]['ID'] ={{verb_fetch[1]['ID']}}

And you can access a column like this:
	verb_fetch.column('NAME') ={{verb_fetch.column('NAME')}}

**3. USING '_Query'**
It allows to retrieve all the queries within 'queries.sql' so  they can pass to the database object

For example:
	{{ '{%' }} set find_ed= _database.find(_Query.ed_by_keyname("Customer")) {{ '%}' }} 
{% set find_ed= _database.find(_Query.ed_by_keyname("Customer")) %}
Returns:
	find_ed['NAME']={{find_ed['NAME']}}
