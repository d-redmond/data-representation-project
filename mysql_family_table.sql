CREATE DATABASE IF NOT EXISTS create_user_table;
CREATE DATABASE mysql_family_table;
USE mysql_family_table;

CREATE TABLE user_family (
  username VARCHAR(50) NOT NULL, 
  password VARCHAR(50), 
  balance float NOT NULL DEFAULT '0', 
  debt float NOT NULL DEFAULT '0',
  PRIMARY KEY (username)
  )
  ENGINE=InnoDB DEFAULT CHARSET=latin1;

create_user_table