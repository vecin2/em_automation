select pk.table_name 
   from   user_constraints fk
join   user_constraints pk
on     pk.constraint_name = fk.r_constraint_name
and    pk.owner = fk.owner
where  fk.constraint_name = '{{constraint_name}}';
