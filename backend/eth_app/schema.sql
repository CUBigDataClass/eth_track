DROP TABLE IF EXISTS ethentry;


CREATE TABLE ethentry (
        time INTEGER PRIMARY KEY,
        blocknumber INTEGER NOT NULL,
        fromaddress VARCHAR(255) NOT NULL,
        toaddress VARCHAR(255) NOT NULL,
        ethvalue INTEGER NOT NULL,
        gas INTEGER NOT NULL,
        gasUsed INTEGER NOT NULL
);
