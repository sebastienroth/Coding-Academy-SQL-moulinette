SELECT REPLACE(profiles.email, 'machin.com', 'coding-academy.fr') AS `New email addresses`
FROM profiles
ORDER BY profiles.email DESC;