CREATE TABLE User (
	id int,
	email text,
	phone text,
	PRIMARY KEY(id)
);

CREATE TABLE Area (
	zip text,
	school_campus text,
	PRIMARY KEY(zip)
);

CREATE TABLE Proposal (
	int id,
	int uid,
	from_time date,
	until_time date,
	ideal_size int,
	minimum_size int,
	maximum_size int,
	price_range int, -- 0 to 4, price range only has 5 options
	pending boolean,
	FOREIGN KEY(uid) REFERENCES User(id),
	PRIMARY KEY(id)
);

CREATE TABLE Meal (
	id int,
	size int,
	time date,
	pending boolean,
	PRIMARY KEY(id)
);

CREATE TABLE Matched (
	mid int,
	pid int,
	PRIMARY KEY(mid)
	FOREIGN KEY(mid) REFERENCES Meal(id),
	FOREIGN KEY(pid) REFERENCES Proposal(id),
);

CREATE TABLE Reservation (
	-- id int,
	mid int,
	size int,
	time date,
	PRIMARY KEY(mid),
	FOREIGN KEY(mid) REFERENCES Meal(id)
);

CREATE TABLE Restaurant (
	id int,
	name text,
	cuisine text,
	open_now boolean,
	price_range int, -- same scale as in Proposal
	website_url text,
	PRIMARY KEY(id)
);