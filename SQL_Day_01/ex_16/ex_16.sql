SELECT MONTHNAME(birthdate) AS 'month of birth'
FROM profiles
WHERE id >= 42 AND
id <=84
ORDER BY id ASC;
