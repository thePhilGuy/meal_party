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
	name text,
	cuisine text,
	open_now boolean,
	price_range int, -- same scale as in Proposal
	website_url text,
	PRIMARY KEY(id),
	FOREIGN KEY(zip) REFERENCES Area(zip) -- Is in relationship
);

CREATE TABLE Proposal (
	id int NOT NULL,
	uid int,
	rid int NULL, -- at relationship
	zip varchar(10), -- in (area) relationship
	from_time date NOT NULL,
	until_time date NOT NULL,
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
	time date,
	pending boolean,
	PRIMARY KEY(id)
);

CREATE TABLE Matched (
	mid int NOT NULL,
	pid int NOT NULL,
	PRIMARY KEY(pid, mid),
	FOREIGN KEY(mid) REFERENCES Meal(id),
	FOREIGN KEY(pid) REFERENCES Proposal(id)
);

CREATE TABLE Reservation (
	id int,
	mid int,
	rid int,
	size int,
	time date,
	PRIMARY KEY(id),
	FOREIGN KEY(mid) REFERENCES Meal(id), -- This is equivalent to the Placed for relationship
	FOREIGN KEY(rid) REFERENCES Restaurant(id)
);