--update agent password
{%if are_you_sure == 'Y' %}
update agent
set PASSWORD = (select PASSWORD from AGENT where username ='{{agent_b | description("Enter the username where the password will be copy from")}}'),
 SALT = (select SALT from agent where username = '{{agent_b}}'),
 EXPIRES = (select EXPIRES from AGENT where USERNAME = '{{agent_b}}'),
 DISABLED ='no'
where USERNAME in ('{{agent_a | suggest([_db.list.agent_usernames()])}}')
{% endif %}
