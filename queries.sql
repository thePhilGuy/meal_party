# Select all proposals between 9/21/15 1pm and 9/22/15 10pm
SELECT * FROM Proposal WHERE from_time > 'September 21 13:00:00 2015 EST' AND until_time <  'September 22 22:00:00 2015 EST' ;

# Select all restaurants on or by a school campus
SELECT Area.school_campus, Restaurant.name
FROM Area
INNER JOIN Restaurant
ON Area.zip=Restaurant.zip
WHERE (Area.school_campus = '') IS FALSE;


SELECT SUM(ideal_size) 
FROM Proposal 
WHERE ideal_size > 2;