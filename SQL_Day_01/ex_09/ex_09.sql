SELECT min_duration AS 'Duration of the shortest movie'
FROM movies
WHERE min_duration > 0
ORDER BY min_duration ASC
LIMIT 1;
