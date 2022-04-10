DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS ethentry;
DROP TABLE IF EXISTS datatype;



CREATE TABLE datatype (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	title TEXT NOT NULL,
	units TEXT NOT NULL,
	description TEXT NOT NULL
);

CREATE TABLE ethentry (
	time DATETIME PRIMARY KEY,
	blocknumber INTEGER NOT NULL,
	fromaddress VARCHAR(255) NOT NULL,
	toaddress VARCHAR(255) NOT NULL,
	ethvalue INTEGER NOT NULL,
	gas INTEGER NOT NULL,
	gasUsed INTEGER NOT NULL
);



INSERT INTO datatype (title, units, description)
	VALUES
	("Positive Contract Transactions", "Eth", "Total transactions to a contract"),
	("Negative Contract Transactions", "Eth", "Total transactions from a contract"),
	("Miner Rewards", "Eth", "Total rewards earned by a miner");
