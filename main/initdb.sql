CREATE DATABASE mysql_family_table;
USE mysql_family_table;

CREATE TABLE family_members (
  username VARCHAR(50) NOT NULL, 
  password VARCHAR(50), 
  balance float NOT NULL DEFAULT '0', 
  debt float NOT NULL DEFAULT '0',
  PRIMARY KEY (username)
  )   ENGINE=InnoDB DEFAULT CHARSET=latin1;


