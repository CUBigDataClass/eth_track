DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS ethentry;
DROP TABLE IF EXISTS datatype;


CREATE TABLE user (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT UNIQUE NOT NULL,
	PASSWORD TEXT NOT NULL
);

CREATE TABLE datatype (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	title TEXT NOT NULL,
	units TEXT NOT NULL,
	description TEXT NOT NULL
);

CREATE TABLE ethentry (
	datakey INTEGER NOT NULL,
	userkey INTEGER NOT NULL,
	volume INTEGER NOT NULL,
	magnitude INTEGER NOT NULL,
	startdate TIMESTAMP NOT NULL,
	enddate TIMESTAMP NOT NULL,
	startblock INTEGER NOT NULL,
	endblock INTEGER NOT NULL,
	FOREIGN KEY (userkey) REFERENCES user (id),
	FOREIGN KEY (datakey) REFERENCES data (id)
);


INSERT INTO datatype (title, units, description)
	VALUES
	("Positive Contract Transactions", "Eth", "Total transactions to a contract"),
	("Negative Contract Transactions", "Eth", "Total transactions from a contract"),
	("Miner Rewards", "Eth", "Total rewards earned by a miner");
