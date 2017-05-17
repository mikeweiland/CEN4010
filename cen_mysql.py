#!/usr/bin/env python3
###############################################################################
# cen_mysql.py
# database initiation
# functions for communicating with the database.
# CEN 4010 Summer 2017 Team 6
###############################################################################
import mysql.connector
from mysql.connector import errorcode
import json

TABLES = {}

TABLES['books'] = (
    "create table books ("
    "  title varchar(255) not null,"
    "  quantity int(255) not null,"
    "  cover_file_name varchar(255) not null,"
    "  genre enum ('scifi', 'iot', 'gaming', 'pickup', 'history') not null,"
    "  rating decimal(3, 2) not null,"
    "  author int not null,"
    "  price double,"
    "  foreign key (author)"
    "  references authors (author_id)"
    "  on delete cascade,"
    "  primary key (title),"
    "  unique (cover_file_name)"
    ") ENGINE=InnoDB")

TABLES['authors'] = (
    "create table authors ("
    "  author_id int not null,"
    "  first_name varchar(255) not null,"
    "  last_name varchar(255) not null,"
    "  bio varchar(2000) not null,"
    "  primary key (author_id)"
    ") ENGINE=InnoDB")

TABLES['users'] = (
    "create table users ("
    "  password varchar(255) not null,"
    "  nickname varchar(255) not null,"
    "  email_address varchar(255) not null,"
    "  home_address varchar(255) not null,"
    "  unique (nickname),"
    "  primary key (email_address)"
    ") ENGINE=InnoDB")

TABLES['credit_cards'] = (
    "create table credit_cards ("
    "  cc_number varchar(255) not null,"
    "  security_code varchar(3) not null,"
    "  expiration varchar(255) not null,"
    "  provider varchar(255) not null,"
    "  first_name varchar(255) not null,"
    "  last_name varchar(255) not null,"
    "  primary key (cc_number)"
    ") ENGINE=InnoDB")

TABLES['tech_valley_times'] = (
    "create table tech_valley_times ("
    "  book varchar(255) not null,"
    "  rating decimal(3, 2) not null,"
    "  foreign key (book)"
    "  references books (title)"
    "  on delete cascade"
    ") ENGINE=InnoDB")

class DB():

    def __init__(self):
        with open('aws_rds_auth.json') as data_file:
            aws_creds = json.load(data_file)
        self.USER = aws_creds["USER"]
        self.HOST = aws_creds["HOST"]
        self.DB_NAME = aws_creds["DB_NAME"]
        self.PASSWORD = aws_creds["PASSWORD"]
        self.cnx, self.cursor = self.connect()
        self.init_db()

    def connect(self):
        db = mysql.connector.connect(
            user = self.USER,
            password = self.PASSWORD,
            host = self.HOST,
            database = self.DB_NAME
        )
        cursor = db.cursor()
        db_cursor = (db, cursor)
        return db_cursor

    def disconnect(self):
        self.cnx.close()
        self.cursor.close()

    def query(self, query):
        try:
            self.cursor.execute(query)
            print(self.cursor.fetchall())
        except mysql.connector.Error as err:
            print(err.msg)

    def create_database(self):
        try:
            self.cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET `utf8`".format(DB_NAME))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    def init_db(self):
        # Create the database if it does not exist yet. Exit if this fails.
        try:
            self.cnx.database = DB_NAME
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                create_database(self.cursor)
                self.cnx.database = DB_NAME
            else:
                print(err)
                exit(1)

        # Try making all the tables defined by each schema at the top of the file.
        for name, schema in TABLES.items():
            try:
                print("Creating table {}: ".format(name), end='')
                self.cursor.execute(schema)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("Ok")
