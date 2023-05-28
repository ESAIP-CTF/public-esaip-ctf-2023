import sqlite3

from os import getenv
from dotenv import load_dotenv

load_dotenv()

FLAG = getenv('FLAG')

conn = sqlite3.connect("data.db")
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS Accounts(
              id INTEGER PRIMARY KEY,
              name TEXT,
              password VARCHAR
            )""")
c.execute("""CREATE TABLE IF NOT EXISTS Balances(
              id INTEGER PRIMARY KEY,
              balance INTEGER,
              overdraft INTEGER
            )""")

users = [
    (1, "Bowser", FLAG),
    (2, "Bowser Jr", "B0wser123"),
    (3, "Kamek", "password"),
    (4, "King Boo", "BoOoOoOOoOoo"),
    (5, "Goomboss", "G0omba_64DS"),
    (6, "Larry Koopa", "kOOpalings<3"),
    (7, "Roy Koopa", "Drag00n"),
    (8, "Wendy O. Koopa", "Il0vejUst1nB1eber"),
    (9, "Iggy Koopa", "Nihihi"),
    (10, "Morton Koopa Jr", "Command3r"),
    (11, "Lemmy Koopa", "Agaboug4"),
    (12, "Ludwig Van Koopa", "LilAloulaliii34")
]
balance = [
    (1, 999_999_999, 1_000_000),
    (2, 10_029_127, 100_000),
    (3, 666, 100_000),
    (4, 992_763_271, 100_000),
    (5, 100_100_001, 100_000),
    (6, -666, 1000),
    (7, 872_923, 1000),
    (8, 123_321, 1000),
    (9, 0, 1000),
    (10, 333, 1000),
    (11, -928, 1000),
    (12, 100_201, 1000) 
]
c.executemany("INSERT INTO Accounts(id, name, password) VALUES(?,?,?)", users)
c.executemany("INSERT INTO Balances(id, balance, overdraft) VALUES(?,?,?)", balance)

conn.commit()

conn.close()

print("SUCCESSFULLY INITIATED THE DATABASE")