SELECT COUNT(title) AS 'Number of movies that starts with "eX"'
FROM movies
WHERE title LIKE 'eX%' collate utf8mb4_bin;
