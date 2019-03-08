SELECT SUBSTRING(movies.summary,1,92) AS `Summaries`
FROM movies
WHERE movies.id%2 != 0
AND movies.id BETWEEN 42 AND 84;