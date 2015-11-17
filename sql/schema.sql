CREATE TABLE Person(
	id serial,
	email text,
	phone text,
	PRIMARY KEY(id)
);

CREATE TABLE Area (
	zip varchar(10) NOT NULL,
	PRIMARY KEY(zip)
);

CREATE TABLE Restaurant (
	id serial,
	zip varchar(10) NOT NULL,
	name text NOT NULL,
	cuisine text,
	website_url text,
	PRIMARY KEY(id),
	FOREIGN KEY(zip) REFERENCES Area(zip) -- Is in relationship
);

CREATE TABLE Proposal (
	id serial,
	uid int NOT NULL,
	cuisine text,
	zip varchar(10) NOT NULL, -- in (area) relationship
	from_time time NOT NULL,
	until_time time NOT NULL,
	CHECK (from_time < until_time), -- from_time is before until_time
	ideal_size int,
	minimum_size int,
	CHECK (minimum_size >= 1),
	maximum_size int,
	CHECK (minimum_size <= maximum_size),
	pending boolean,
	PRIMARY KEY(id),
	FOREIGN KEY(uid) REFERENCES Person(id),
	FOREIGN KEY(zip) REFERENCES Area(zip)
);

CREATE TABLE Meal (
	me_id int NOT NULL,
	size int,
	ideal_size int,
	CHECK (size > 1),
	mtime timestamp,
	pending boolean,
	PRIMARY KEY(me_id)
);

CREATE TABLE Matched (
	mid int NOT NULL,
	pid int NOT NULL,
	PRIMARY KEY(mid, pid),
	FOREIGN KEY(mid) REFERENCES Meal(me_id),
	FOREIGN KEY(pid) REFERENCES Proposal(id)
);


-- #changes:
-- ###############################
-- # add cuisine to proposal 
-- # change meal.id to meal.me_id
-- # add ideal_size to Meal
-- # add constraint to schema start time <= endtime - 30 min (maybe)
-- # save latitude and longitude  to restaurant (maybe)