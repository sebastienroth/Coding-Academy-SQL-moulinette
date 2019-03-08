SELECT profiles.zipcode AS `Zip codes`
FROM profiles
GROUP BY profiles.zipcode
HAVING COUNT(profiles.zipcode) > 1
ORDER BY profiles.zipcode ASC;