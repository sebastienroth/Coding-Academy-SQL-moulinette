SELECT title AS 'Title of the longest movie'
FROM movies
ORDER BY min_duration DESC
LIMIT 1;
