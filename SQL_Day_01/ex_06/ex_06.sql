SELECT title AS 'Title of the last 42 movies'
FROM movies
ORDER BY id DESC
LIMIT 42;
