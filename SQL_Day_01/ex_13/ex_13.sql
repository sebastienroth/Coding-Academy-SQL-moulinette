SELECT room_number AS 'Room numbers',
       name AS 'Room names'
FROM rooms
WHERE seats > 0
AND floor <> 1;
