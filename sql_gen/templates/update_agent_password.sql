--update agent password
{% set usernames =_db.fetch.all_agents().column("USERNAME")%}
update agent
set PASSWORD = (select PASSWORD from AGENT where username ='{{username_to_copy_from | description("Enter the username where the password will be copy from")}}'),
 SALT = (select SALT from agent where username = '{{username_to_copy_from}}'),
 EXPIRES = (select EXPIRES from AGENT where USERNAME = '{{username_to_copy_from}}'),
 DISABLED ='no'
where USERNAME in ('{{username | suggest(usernames)}}');
