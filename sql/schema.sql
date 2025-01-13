PRAGMA foreign_keys = ON;
CREATE TABLE users(
  email    VARCHAR(40) NOT NULL,
  firstname VARCHAR(40) NOT NULL,
  lastname VARCHAR(40) NOT NULL,
  imagelink TEXT NOT NULL,
  created  DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(email)
);

CREATE TABLE certificates(
  certid   INTEGER PRIMARY KEY AUTOINCREMENT,
  Name          TEXT,
  Abbr          TEXT,
  Organization  TEXT, 
  Time          TEXT, 
  Cost          TEXT,
  Industry      TEXT,
  Link          TEXT,
  BudgetIndex   INTEGER,
  TimeIndex     INTEGER
);

CREATE TABLE keywords(
  email TEXT,
  keyword TEXT
);

CREATE TABLE budget(
  email TEXT,
  cost INTEGER
);

CREATE TABLE time(
  email TEXT,
  time INTEGER
);


CREATE TABLE status(
  email VARCHAR(40) NOT NULL,
  certid INTEGER NOT NULL,
  created DATETIME DEFAULT CURRENT_TIMESTAMP,
  value CHAR(1) NOT NULL,
  PRIMARY KEY(email, certid)
  FOREIGN KEY(email) REFERENCES users(email) ON DELETE CASCADE 
  FOREIGN KEY(certid) REFERENCES certs(certid) ON DELETE CASCADE
  FOREIGN KEY(value) REFERENCES statustype(type)
);

CREATE TABLE statustype(
  type CHAR(1) PRIMARY KEY NOT NULL
);

CREATE TABLE resumes(
  filename VARCHAR(40) NOT NULL,
  username VARCHAR(40) NOT NULL,
  created DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE matches(
  username VARCHAR(40) NOT NULL,
  certid INTEGER NOT NULL,
  keycount INTEGER NOT NULL,
  PRIMARY KEY(username, certid)
  FOREIGN KEY(username) REFERENCES users(email) ON DELETE CASCADE 
  FOREIGN KEY(certid) REFERENCES certs(certid) ON DELETE CASCADE
);