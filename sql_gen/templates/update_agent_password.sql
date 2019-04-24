
--update agent password
update agent
set PASSWORD = (select PASSWORD from AGENT where username ='{{user_to_copy_password_from}}'),
 SALT = (select SALT from agent where username = '{{user_to_copy_password_from}}'),
 EXPIRES = (select EXPIRES from AGENT where USERNAME = '{{user_to_copy_password_from}}'),
 DISABLED ='no'
where USERNAME in ('{{username}}')

