

DROP DATABASE IF EXISTS foodzilla;
CREATE DATABASE foodzilla;


USE foodzilla;

DROP TABLE IF EXISTS RESTAURANT;
CREATE TABLE RESTAURANT (
  rname        varchar(25) not null,
  rid    int not null,
  mgrid      char(9) not null,
  CONSTRAINT pk_Restaurant primary key (rid)
  -- CONSTRAINT uk_rname UNIQUE (rname) 
);

INSERT INTO RESTAURANT VALUES ('Arby\'s', 1, '333445555');
INSERT INTO RESTAURANT VALUES ('Chili\'s', 2, '987654321');
INSERT INTO RESTAURANT VALUES ('Olive Garden', 3, '123456789');
INSERT INTO RESTAURANT VALUES ('Wendy\'s', 4, '111111119');

SELECT * FROM RESTAURANT;