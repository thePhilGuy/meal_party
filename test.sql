INSERT INTO Person(id, email, phone) VALUES (0, 'dafsd@fsdfsd.com', '9112345671'), (1, 'sdf@fsdf.com', '1111111111');
SELECT * FROM Person;
INSERT INTO Area VALUES ('10027', 'Columbia University');
INSERT INTO Proposal(id, uid, zip, from_time, until_time, ideal_size, minimum_size, maximum_size, price_range, pending)
VALUES 
  (0, 0, '10027', 'September 29 12:00:00 2015 EST', 'September 29 15:00:00 2015 EST', 3, 2, 5, 1, true), 
  (1, 1, '10027', 'September 29 12:00:00 2015 EST', 'September 29 15:00:00 2015 EST', 3, 2, 5, 1, true);
INSERT INTO Meal VALUES (0, 2, 'September 29 12:00:00 2015 EST', true);
INSERT INTO Matched VALUES (0, 0), (0, 1);
SELECT * FROM Matched;
UPDATE Meal SET pending = false WHERE id = 0;
SELECT * FROM Meal;
UPDATE Proposal SET pending = false WHERE id = 0 or id = 1;
SELECT * FROM Proposal;
INSERT INTO Restaurant(id, zip, name, open_now, price_range) 
VALUES (0, '10027', 'Ollies', true, 0);
SELECT * FROM Restaurant;
INSERT INTO Reservation(mid, rid, size, rtime) 
VAlUES (0, 0, 2, 'September 29 12:00:00 2015 EST');
SELECT * FROM Reservation;