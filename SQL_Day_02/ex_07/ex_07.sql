SELECT movies.title AS `Movie title`
FROM movies
WHERE SUBSTRING(movies.title,1,1) BETWEEN 'O' AND 'T'
ORDER BY movies.title ASC;