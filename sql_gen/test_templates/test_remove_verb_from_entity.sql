--["Customer","inlineSearch"]
DELETE
FROM EVA_VERB
WHERE NAME='inlineSearch'
and ENTITY_DEF_ID=@ED.Customer;

DELETE
FROM CCADMIN_IDMAP
WHERE KEYSET = 'V'
AND ID =@V.InlineSearchCustomer;
