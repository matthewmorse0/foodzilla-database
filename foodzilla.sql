

DROP DATABASE IF EXISTS foodzilla;
CREATE DATABASE foodzilla;


USE foodzilla;

DROP TABLE IF EXISTS RESTAURANT;
CREATE TABLE RESTAURANT (
  rname        varchar(25) not null,
  rid    int not null,
  mgrid      char(9) not null,
  waitTime      int not null,
  waitlist    int,
  menuLink char(50) not null,
  -- diningTables is a string where each character is a digit from 0-9, 0 representing 10
  -- Each digit represents a table and how many people can be seated there, iterating through rows top to bottom, left to right
  diningTables char(64),
  -- freeTables is a string of 0s (taken) and 1s (free) indicating whether the corresponding table in diningTables is taken or free
  freeTables char(64),
  CONSTRAINT pk_Restaurant primary key (rid)
);

DROP TABLE IF EXISTS RINFO;
CREATE TABLE RINFO (
  rid         int not null,
  numTables   int,
  numCust     int,
  custTime    int
);

DROP TABLE IF EXISTS SEATING;
CREATE TABLE SEATING (
	rid			int,
	tbid		int,
  avaliable  boolean,
	stime		Time,
	CONSTRAINT pk_Table primary key (rid, tbid)
);


INSERT INTO RESTAURANT VALUES ('King Street Pub', 1, '333445555', 30, 0, 'https://www.kingstreetpub.com/', '00404050|05020208|30400500', '00101000|00010000|10000100');
INSERT INTO RESTAURANT VALUES ('Chili\'s', 2, '987654321', 20, 0, 'https://chilis.com/', '00009000|30303030|00000000', '00000000|00000000|00000000');
INSERT INTO RESTAURANT VALUES ('Olive Garden', 3, '123456789', 10, 0, 'https://www.olivegarden.com/home', '60000302|00060002|50000004', '10000001|00010000|10000001');
INSERT INTO RESTAURANT VALUES ('Dion\'s', 4, '111111119', 10, 0, 'https://order.dions.com/#/restaurantSearch', '08020080|40004004|20202020', '01010000|00001000|10101010');
INSERT INTO RINFO VALUES (1, 10, 1, 1800);
INSERT INTO RINFO VALUES (2, 5, 1, 1800);
INSERT INTO RINFO VALUES (3, 7, 1, 1800);
INSERT INTO RINFO VALUES (4, 10, 1, 1800);

SELECT * FROM RESTAURANT;