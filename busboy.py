#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# dbtools.py
# Author: Germain GAILLARD <gaillard.germain@gmail.com>
# Version: 0.1
# License: GNU GPL


from mysql.connector import Error, errorcode
from dbtools import Dbtools


class Busboy:
    def __init__(self):
        self.conx = Dbtools.connect()
        self.cursor = self.conx.cursor()

    def dismiss(self):
        """ Close connexion to MySQL database """

        self.cursor.close()
        self.conx.close()
        print('Connection closed.')

    def groups_menu(self):
        """ Returns a dict of alimentary groups with their id """

        query = 'SELECT * FROM Categories ORDER BY id'
        menu = {}

        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            for row in rows:
                menu[str(row[0])] = row[1]

        except Error as error:
            print(error)

        return menu

    def products_menu(self, id):
        """ Returns a dict of random top ten 'bads' products with their id """

        query = "SELECT id, name, brand \
                 FROM Products WHERE categories_id = {} \
                 AND (nutriscore IN ('d', 'e') \
                 OR nutriscore IS NULL) \
                 ORDER BY RAND() LIMIT 10".format(id)
        menu = {}

        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            for row in rows:
                menu[str(row[0])] = '{} de {}'.format(row[1], row[2])

        except Error as error:
            print(error)

        return menu

    def keyword(self, id):
        """ Returns the keyword of the product """

        query = "SELECT compared_to FROM Products WHERE id = {}".format(id)
        keyword = None

        try:
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            keyword = row[0]

        except Error as error:
            print(error)

        return keyword

    def substitut_id(self, id):
        """ Returns random 'good' product's id which tags matched keyword """

        keyword = self.keyword(id)
        query = "SELECT id FROM Products WHERE tags LIKE ('%{}%') \
                 AND (nutriscore IN ('a', 'b', 'c') OR additives IS NULL) \
                 AND id <> {} \
                 ORDER BY RAND() LIMIT 1".format(keyword, id)
        id = None

        try:
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            if row:
                id = row[0]

        except Error as error:
            print(error)

        return id

    def product_detail(self, id):
        """ Returns a dict {field : value} of the product """

        query = "SELECT * FROM Products WHERE id = {}".format(id)
        product = {}

        try:
            self.cursor.execute(query)
            row = self.cursor.fetchone()

            if row:
                product['Nom'] = row[1]
                product['Marque'] = row[2]
                product['Ingrédients'] = row[5]
                product['Additifs'] = row[6]
                product['Allergènes'] = row[7]
                product['Nutriscore'] = row[8]
                product['Labels'] = row[9]
                product['Distribué par'] = row[10]
                product['Lien OpenFoodFacts'] = row[11]

        except Error as error:
            if error.errno == errorcode.ER_BAD_FIELD_ERROR:
                print("\nAucun produits correspondant\n")
            else:
                print(error)

        return product

    def save(self, ids):
        """ Saves comparison in database (product's id) """

        query = "INSERT INTO Favorites(unliked_id, liked_id) \
                 VALUES(%s, %s)"

        try:
            self.cursor.execute(query, ids)
            self.conx.commit()

        except Error as error:
            print(error)

    def substituts_saved(self):
        """ Returns a dict of comparisons :
            {id : [unliked_id, unliked_name, unliked_brand,
            liked_id, liked_name, liked_brand]...} """

        query = "SELECT Favorites.id, unliked_id, Prod1.name, Prod1.brand,\
                 liked_id, Prod2.name, Prod2.brand \
                 FROM Favorites INNER JOIN Products AS Prod1 \
                 ON Favorites.unliked_id = Prod1.id \
                 INNER JOIN Products AS Prod2 \
                 ON Favorites.liked_id = Prod2.id"
        sub = {}

        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            for row in rows:
                row = list(row)
                id = row.pop(0)
                sub[str(id)] = row

        except Error as error:
            print(error)

        return sub
