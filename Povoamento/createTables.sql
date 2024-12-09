-- Tabela Person
CREATE TABLE Person (
    ID INTEGER PRIMARY KEY NOT NULL,
    Name VARCHAR(50) NOT NULL
);

-- Tabela Media
CREATE TABLE Media (
    ID INTEGER PRIMARY KEY NOT NULL,
    TypeID INTEGER NOT NULL,
    Title VARCHAR(200) NOT NULL,
    Date_Added DATE,
    Release_year INTEGER,
    Rating VARCHAR(20),
    Duration VARCHAR(50),
    Description TEXT,
    FOREIGN KEY (TypeID) REFERENCES Type (ID)
);

-- Tabela Type
CREATE TABLE Type (
    ID INTEGER PRIMARY KEY NOT NULL,
    Name VARCHAR(15) NOT NULL
);

-- Tabela Genre
CREATE TABLE Genre (
    ID INTEGER PRIMARY KEY NOT NULL,
    Name VARCHAR(50) NOT NULL
);

-- Tabela MediaGenre (relação muitos-para-muitos entre Media e Genre)
CREATE TABLE MediaGenre (
    MediaID INTEGER NOT NULL,
    GenreID INTEGER NOT NULL,
    PRIMARY KEY (MediaID, GenreID),
    FOREIGN KEY (MediaID) REFERENCES Media (ID),
    FOREIGN KEY (GenreID) REFERENCES Genre (ID)
);

-- Tabela Country
CREATE TABLE Country (
    ID INTEGER PRIMARY KEY NOT NULL,
    Name VARCHAR(50) NOT NULL
);

-- Tabela MediaCountry (relação muitos-para-muitos entre Media e Country)
CREATE TABLE MediaCountry (
    MediaID INTEGER NOT NULL,
    CountryID INTEGER NOT NULL,
    PRIMARY KEY (MediaID, CountryID),
    FOREIGN KEY (MediaID) REFERENCES Media (ID),
    FOREIGN KEY (CountryID) REFERENCES Country (ID)
);

-- Tabela Cast (relação muitos-para-muitos entre Media e Person)
CREATE TABLE Cast (
    MediaID INTEGER NOT NULL,
    PersonID INTEGER NOT NULL,
    PRIMARY KEY (MediaID, PersonID),
    FOREIGN KEY (MediaID) REFERENCES Media (ID),
    FOREIGN KEY (PersonID) REFERENCES Person (ID)
);

-- Tabela Director (relação muitos-para-muitos entre Media e Person)
CREATE TABLE Director (
    MediaID INTEGER NOT NULL,
    PersonID INTEGER NOT NULL,
    PRIMARY KEY (MediaID, PersonID),
    FOREIGN KEY (MediaID) REFERENCES Media (ID),
    FOREIGN KEY (PersonID) REFERENCES Person (ID)
);
