SELECT name AS 'Name of the most expensive subscription'
, price AS Price
FROM subscriptions
ORDER BY price DESC
LIMIT 1;
