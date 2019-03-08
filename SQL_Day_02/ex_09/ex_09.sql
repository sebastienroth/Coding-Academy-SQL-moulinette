SELECT movies.title, movies.min_duration 
FROM movies
ORDER BY LENGTH(movies.title) DESC, movies.min_duration ASC;