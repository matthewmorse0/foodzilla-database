

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

DROP TABLE IF EXISTS MENU;
CREATE TABLE MENU (
  menuid      char(4) not null,
  rid      int not null,
  items char(100),
  CONSTRAINT pk_Menu primary key (menuid),
  CONSTRAINT fk_Menu foreign key (rid) references RESTAURANT (rid)
);

INSERT INTO RESTAURANT VALUES ('Arby\'s', 1, '333445555');
INSERT INTO RESTAURANT VALUES ('Chili\'s', 2, '987654321');
INSERT INTO RESTAURANT VALUES ('Olive Garden', 3, '123456789');
INSERT INTO RESTAURANT VALUES ('Wendy\'s', 4, '111111119');

INSERT INTO MENU VALUES ('1111', 1, 'Beef, Sandwich, The Meats');
INSERT INTO MENU VALUES ('2222', 2, 'Crispy Honey Chipotle Chicken Crispers, Quesadilla');
INSERT INTO MENU VALUES ('3333', 3, 'Unlimited Soup/Salad/Breadsticks, Alfredo, Family');
INSERT INTO MENU VALUES ('4444', 4, '4 for 4, Nuggs');

SELECT * FROM RESTAURANT;
SELECT * FROM MENU;