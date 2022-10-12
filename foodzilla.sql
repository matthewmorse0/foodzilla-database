

DROP DATABASE IF EXISTS foodzilla;
CREATE DATABASE foodzilla;


USE foodzilla;

DROP TABLE IF EXISTS DEPARTMENT;
CREATE TABLE DEPARTMENT (
  dname        varchar(25) not null,
  did    int not null,
  mgrid      char(9) not null,
  CONSTRAINT pk_Department primary key (did),
  CONSTRAINT uk_dname UNIQUE (dname) 
);

INSERT INTO DEPARTMENT VALUES ('Pediatrics', 5, '333445555');
INSERT INTO DEPARTMENT VALUES ('Administration', 4, '987654321');
INSERT INTO DEPARTMENT VALUES ('Orthopedics', 3, '123456789');
INSERT INTO DEPARTMENT VALUES ('Neurosurgery', 2, '111111119');

SELECT * FROM DEPARTMENT;