import sqlite3
from sqlite3 import Error
import pandas
# pip install psycopg2
import psycopg2
from abc import ABC, abstractmethod


class DataClient(ABC):
    @abstractmethod
    def _get_connection(self):
        pass

    @abstractmethod
    def create_mebel_table(self, conn):
        pass

    @abstractmethod
    def get_items(self, conn, price_from=0, price_to=100000):
        pass

    @abstractmethod
    def insert(self, conn, link, price, description):
        pass

    @abstractmethod
    def select_by_word(self, word):
        pass

    @abstractmethod
    def select_by_word_and_price(self, word, price_from, price_to):
        pass

    def run_test(self):
        conn = self._get_connection()
        if not isinstance(conn, str):
            self.create_mebel_table(conn)
            items = self.get_items(conn, price_from=10, price_to=30)
            [print(item) for item in items]
            conn.close()
        else:
            print(self.get_items(conn, price_from=10, price_to=30).to_string())


class PostgresClient(DataClient):
    USER = "postgres"
    PASSWORD = "postgres"
    HOST = "172.17.135.17"
    PORT = "5432"

    def _get_connection(self):
        # try:
        #     connection = psycopg2.connect(
        #         user=self.USER,
        #         password=self.PASSWORD,
        #         host=self.HOST,
        #         port=self.PORT
        #     )
        #     return connection
        # except Error:
        #     print(Error)
        return psycopg2.connect(
            user=self.USER,
            password=self.PASSWORD,
            host=self.HOST,
            port=self.PORT
        )

    def select_by_word(self, word):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM app_1_mebel WHERE description LIKE '%s'", (word,))
            return cursor.fetchall()

    def select_by_word_and_price(self, word, price_from, price_to):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM app_1_mebel WHERE description LIKE %s and price >= %s and price <= %s",
                (f'%{word}%', price_from, price_to)
            )
            return cursor.fetchall()

    def create_mebel_table(self, conn):
        cursor_object = conn.cursor()
        cursor_object.execute(
            """
                CREATE TABLE IF NOT EXISTS app_1_mebel
                (
                    id serial PRIMARY KEY, 
                    link text, 
                    price integer, 
                    description text
                )
            """
        )
        conn.commit()

    def get_items(self, conn, price_from=0, price_to=100000):
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM app_1_mebel WHERE price >= {price_from} and price <= {price_to}')
        return cursor.fetchall()

    def insert(self, conn, link, price, description):
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO app_1_mebel (link, price, description) VALUES ('{link}', '{price}', '{description}')")
        conn.commit()


class Sqlite3Client(DataClient):
    DB_NAME = "mebel.db"

    def _get_connection(self):
        try:
            conn = sqlite3.connect(self.DB_NAME)
            return conn
        except Error:
            print(Error)

    def create_mebel_table(self, conn):
        cursor_object = conn.cursor()
        cursor_object.execute(
            """
                CREATE TABLE IF NOT EXISTS mebel
                (
                    id integer PRIMARY KEY autoincrement, 
                    link text, 
                    price integer, 
                    description text
                )
            """
        )
        conn.commit()

    def get_items(self, conn, price_from=0, price_to=100000):
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM mebel WHERE price >= {price_from} and price <= {price_to}')
        return cursor.fetchall()

    def insert(self, conn, link, price, description):
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO mebel (link, price, description) VALUES ('{link}', '{price}', '{description}')")
        conn.commit()

    def select_by_word(self, word):
        pass

    def select_by_word_and_price(self, word, price_from, price_to):
        pass


class CsvClient(DataClient):
    DB_NAME = "mebel.csv"

    def _get_connection(self):
        return self.DB_NAME

    def create_mebel_table(self, conn):
        pandas.DataFrame({'link': [], 'price': [], 'description': []}).to_csv(self.DB_NAME, index=False)

    def get_items(self, conn, price_from=0, price_to=100000):
        data = pandas.read_csv(self.DB_NAME)
        return data.query('price > @price_from & price < @price_to')

    def insert(self, conn, link, price, description):
        data = pandas.DataFrame([{'link': link, 'price': price, 'description': description}])
        data.to_csv(conn, mode='a', index=False, header=False)

    def select_by_word(self, word):
        pass

    def select_by_word_and_price(self, word, price_from, price_to):
        pass
# PostgresClient().run_test()
# Sqlite3Client().run_test()
# CsvClient().run_test()
