-- {"agent_to_copy_password_from":"admin","agent_username":"agent"}
update agent
set PASSWORD = (select PASSWORD from AGENT where username ='admin'),
 SALT = (select SALT from agent where username = 'admin'),
 EXPIRES = (select EXPIRES from AGENT where USERNAME = 'admin'),
 DISABLED ='no'
where USERNAME in ('agent')
