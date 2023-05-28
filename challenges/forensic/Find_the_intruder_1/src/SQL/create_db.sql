CREATE TABLE users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	first_name VARCHAR(255) NOT NULL,
	last_name VARCHAR(255) NOT NULL,
	gender VARCHAR(255) NOT NULL,
	email VARCHAR(255) NOT NULL,
	password VARCHAR(255) NOT NULL
);

CREATE TABLE connection_logs (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER NOT NULL,
	date datetime datetime default current_timestamp NOT NULL,
	ip_address VARCHAR(255) NOT NULL
);