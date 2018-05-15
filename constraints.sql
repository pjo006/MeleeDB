BEGIN TRANSACTION;

ALTER TABLE characters RENAME TO characters_old;

CREATE TABLE characters(
    Name TEXT PRIMARY KEY,
    Series TEXT NOT NULL,
    Tier TEXT NOT NULL CHECK (Tier IN ('G', 'F', 'E', 'D', 'C', 'B', 'A', 'S', 'SS'))
);

INSERT INTO characters (Name, Series, Tier)
SELECT Name, Series, Tier
FROM characters_old;

DROP TABLE characters_old;



UPDATE players
SET Rank_2013 = NULL
WHERE Rank_2013 = '';

UPDATE players
SET Rank_2014 = NULL
WHERE Rank_2014 = '';

UPDATE players
SET Rank_2015 = NULL
WHERE Rank_2015 = '';

UPDATE players
SET Rank_2016 = NULL
WHERE Rank_2016 = '';

UPDATE players
SET Rank_2017 = NULL
WHERE Rank_2017 = '';

ALTER TABLE players RENAME TO players_old;

CREATE TABLE players(
    Tag TEXT PRIMARY KEY,
    Nationality TEXT NOT NULL,
    Character_1 TEXT NOT NULL,
	Character_2 TEXT,
	Character_3 TEXT,
	Rank_2013 INT CHECK ((Rank_2013 <= 100 AND Rank_2013 >= 1) OR (Rank_2013 IS NULL)),
	Rank_2014 INT CHECK ((Rank_2014 <= 100 AND Rank_2014 >= 1) OR (Rank_2014 IS NULL)),
	Rank_2015 INT CHECK ((Rank_2015 <= 100 AND Rank_2015 >= 1) OR (Rank_2015 IS NULL)),
	Rank_2016 INT CHECK ((Rank_2016 <= 100 AND Rank_2016 >= 1) OR (Rank_2016 IS NULL)),
	Rank_2017 INT CHECK ((Rank_2017 <= 100 AND Rank_2017 >= 1) OR (Rank_2017 IS NULL)),
	FOREIGN KEY (Character_1) REFERENCES characters(Name),
	FOREIGN KEY (Character_2) REFERENCES characters(Name),
	FOREIGN KEY (Character_3) REFERENCES characters(Name)
);

INSERT INTO players (Tag, Nationality, Character_1, Character_2, Character_3, Rank_2013, Rank_2014, Rank_2015, Rank_2016, Rank_2017)
SELECT Tag, Nationality, Character_1, Character_2, Character_3, Rank_2013, Rank_2014, Rank_2015, Rank_2016, Rank_2017
FROM players_old;

DROP TABLE players_old;



ALTER TABLE tournaments RENAME TO tournaments_old;

CREATE TABLE tournaments(
    Name TEXT PRIMARY KEY,
    Entrants INT NOT NULL CHECK (Entrants >= 0),
    Country TEXT NOT NULL,
	City TEXT NOT NULL,
	State TEXT,
	Date TEXT NOT NULL CHECK (Date >= "2001-11-21"),
	Prize_Pool INT NOT NULL CHECK (Prize_Pool >= 0),
	Winner TEXT NOT NULL,
	Place_2 TEXT NOT NULL,
	Place_3 TEXT NOT NULL,
	Place_4 TEXT NOT NULL,
	Place_5 TEXT NOT NULL,
	Place_6 TEXT NOT NULL,
	Place_7 TEXT NOT NULL,
	Place_8 TEXT NOT NULL,
	FOREIGN KEY (Winner) REFERENCES players(Tag),
	FOREIGN KEY (Place_2) REFERENCES players(Tag),
	FOREIGN KEY (Place_3) REFERENCES players(Tag),
	FOREIGN KEY (Place_4) REFERENCES players(Tag),
	FOREIGN KEY (Place_5) REFERENCES players(Tag),
	FOREIGN KEY (Place_6) REFERENCES players(Tag),
	FOREIGN KEY (Place_7) REFERENCES players(Tag),
	FOREIGN KEY (Place_8) REFERENCES players(Tag)
);

INSERT INTO tournaments (Name, Entrants, Country, City, State, Date, Prize_Pool, Winner, Place_2, Place_3, Place_4, Place_5, Place_6, Place_7, Place_8)
SELECT Name, Entrants, Country, City, State, Date, Prize_Pool, Winner, Place_2, Place_3, Place_4, Place_5, Place_6, Place_7, Place_8
FROM tournaments_old;

DROP TABLE tournaments_old;


COMMIT;
