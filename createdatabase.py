import sqlite3 as sql

conn = sql.connect("database.db")
print("Database Created")

#Creating our Usertable in an SQLite environment
conn.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, firstname TEXT, lastname TEXT, email VARCHAR, password VARCHAR, bsrcolor TEXT)')

#Creating our Signal TABLE
conn.execute('CREATE TABLE images (id INTEGER PRIMARY KEY , trend TEXT, filename VARCHAR, bsrcolor TEXT, description TEXT, tag TEXT, redvotes INT, bluevotes INT, yellowvotes INT, greenvotes INT, teachervote VARCHAR, hottness VARCHAR)')
conn.close()

'''From command prompt - or Terminal - Activate this script at
first use with python createdatabase.py
to create tables needed for application.'''
