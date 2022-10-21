DROP TABLE IF EXISTS POSTS;

CREATE TABLE POSTS(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	post_date TIMESTAMP,
	created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	content TEXT,
	author VARCHAR(40),
	platform VARCHAR(20),
	url TEXT,
	keyword VARCHAR(100),
    unique (url, platform) ON CONFLICT FAIL
--                   Maybe a second keyword column
);

