SELECT title FROM movies
WHERE genre_id IN
(SELECT id FROM genres WHERE name = 'romance' OR name = 'action');
