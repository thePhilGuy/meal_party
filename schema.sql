CREATE TABLE Person(
	id int NOT NULL,
	email text,
	phone text,
	PRIMARY KEY(id)
);

CREATE TABLE Area (
	zip varchar(10) NOT NULL,
	school_campus text,
	PRIMARY KEY(zip)
);

CREATE TABLE Restaurant (
	id int NOT NULL,
	zip varchar(10) NOT NULL,
	name text NOT NULL,
	cuisine text,
	open_now boolean NOT NULL,
	price_range int, -- same scale as in Proposal
	website_url text,
	PRIMARY KEY(id),
	FOREIGN KEY(zip) REFERENCES Area(zip) -- Is in relationship
);

CREATE TABLE Proposal (
	id int NOT NULL,
	uid int NOT NULL,
	rid int NULL, -- at relationship
	zip varchar(10) NOT NULL, -- in (area) relationship
	from_time timestamp NOT NULL,
	until_time timestamp NOT NULL,
	ideal_size int,
	minimum_size int,
	maximum_size int,
	price_range int, -- 0 to 4, price range only has 5 options
	pending boolean,
	PRIMARY KEY(id),
	FOREIGN KEY(uid) REFERENCES Person(id),
	FOREIGN KEY(rid) REFERENCES Restaurant(id), -- at relationship
	FOREIGN KEY(zip) REFERENCES Area(zip)
);

CREATE TABLE Meal (
	id int NOT NULL,
	size int,
	mtime timestamp,
	pending boolean,
	PRIMARY KEY(id)
);

CREATE TABLE Matched (
	mid int NOT NULL,
	pid int NOT NULL,
	PRIMARY KEY(mid, pid),
	FOREIGN KEY(mid) REFERENCES Meal(id),
	FOREIGN KEY(pid) REFERENCES Proposal(id)
);

CREATE TABLE Reservation (
	mid int,
	rid int NOT NULL,
	size int,
	rtime timestamp,
	PRIMARY KEY(mid),
	FOREIGN KEY(mid) REFERENCES Meal(id), -- This is equivalent to the Placed for relationship
	FOREIGN KEY(rid) REFERENCES Restaurant(id)
);