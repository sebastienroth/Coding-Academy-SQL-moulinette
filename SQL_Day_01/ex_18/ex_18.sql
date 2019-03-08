SELECT CONCAT_WS('-',CONCAT(UCASE(LEFT(lastname,1)),SUBSTRING(lastname,2)),CONCAT(UCASE(LEFT(firstname,1)),SUBSTRING(firstname,2)))
AS 'Full name'
FROM profiles
ORDER BY birthdate DESC;
