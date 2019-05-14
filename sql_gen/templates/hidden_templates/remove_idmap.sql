DELETE
FROM CCADMIN_IDMAP
WHERE KEYSET = '{{keyset}}'
AND ID =@{{keyset}}.{{keyname}};
