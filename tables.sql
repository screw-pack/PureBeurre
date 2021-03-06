SET NAMES utf8;

DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS PnnsGroups;

CREATE TABLE Products(
  id smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  name varchar(100) NOT NULL UNIQUE,
  brand varchar(100) DEFAULT NULL,
  tags text NOT NULL,
  pnns_group_id smallint(5) unsigned NOT NULL,
  ingredients text DEFAULT NULL,
  additives text DEFAULT NULL,
  allergens text DEFAULT NULL,
  nutriscore varchar(1) DEFAULT NULL,
  labels text DEFAULT NULL,
  stores text DEFAULT NULL,
  link varchar(100) DEFAULT NULL UNIQUE,
  compared_to varchar(50) DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE = InnoDB;

CREATE TABLE PnnsGroups(
  id smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  name varchar(50) NOT NULL UNIQUE,
  PRIMARY KEY (id)
) ENGINE = InnoDB;

CREATE TABLE Substituts (
  id smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  unliked_id smallint(5) unsigned NOT NULL,
  liked_id smallint(5) unsigned NOT NULL,
  PRIMARY KEY (id)
) ENGINE = InnoDB;

LOCK TABLES PnnsGroups WRITE;
INSERT INTO PnnsGroups VALUES (1, 'Lait et produits laitiers'),
(2, 'Viandes Poissons Oeufs'), (3, 'Féculents'), (4, 'Fruits et légumes'),
(5, 'Corps gras'), (6, 'Produits sucrés'), (7, 'Boissons'),
(8, 'Produits salés'), (9, 'Plats préparés'), (10, 'Autre');
UNLOCK TABLES;

ALTER TABLE Products ADD CONSTRAINT fk_pnns_group_id FOREIGN KEY (pnns_group_id) REFERENCES PnnsGroups(id);
ALTER TABLE Substituts ADD CONSTRAINT fk_unliked_id FOREIGN KEY (unliked_id) REFERENCES Products (id);
ALTER TABLE Substituts ADD CONSTRAINT fk_liked_id FOREIGN KEY (liked_id) REFERENCES Products (id);
