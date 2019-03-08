SELECT COUNT(title) AS 'Number of western movies'
FROM movies
WHERE genre_id IN
(SELECT id FROM genres WHERE name = 'western')
AND
(producer_id IN
(SELECT id FROM producers WHERE name = 'tartan movies' OR name = 'lionsgate uk'));
