SELECT rooms.floor AS `Floor number`, SUM(rooms.seats) AS `Total number of seats`, COUNT(rooms.id) AS `Total number of rooms`
FROM rooms
GROUP BY rooms.floor
ORDER BY SUM(rooms.seats) ASC;