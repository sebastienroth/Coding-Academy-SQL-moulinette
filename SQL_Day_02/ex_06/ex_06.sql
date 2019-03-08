SELECT movies.title AS `Movie title`, DATEDIFF(CURDATE(),movies.release_date) AS `Number of days passed`
FROM movies
WHERE movies.release_date != 0000-00-00;