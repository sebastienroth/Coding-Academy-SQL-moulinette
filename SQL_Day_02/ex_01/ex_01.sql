SELECT COUNT(member.id) AS `Number of members`, FLOOR(AVG(DATEDIFF(CURRENT_TIMESTAMP(),profiles.birthdate)/365)) AS `Average age`
FROM member
INNER JOIN profiles ON member.profile_id=profiles.id;
