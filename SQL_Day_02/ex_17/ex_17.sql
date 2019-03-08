SET @producer  = (
	SELECT movies.producer_id
	FROM movies
	INNER JOIN producers ON movies.producer_id=producers.id
	AND producers.name LIKE '%film'
	GROUP BY movies.producer_id
	ORDER BY COUNT(movies.id) ASC
	LIMIT 1
);

UPDATE movies
SET movies.producer_id = @producer
WHERE movies.producer_id IS NULL;
