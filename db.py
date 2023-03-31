# db.py

import sqlite3
from tabulate import tabulate
import pandas as pd
from logger import get_logger

DB_NAME = 'SPEEDTEST_DB'
TABLE_NAME = 'speedtest_data'

_logger = get_logger()

# create database
def connect_db(DB_NAME):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        _logger.info(f"Connected to database {DB_NAME}")
    except Exception as e:
        _logger.error("Failed with exception {}".format(e))
    return conn, cursor

def create_table():
    # create table
    conn, cursor = connect_db(DB_NAME)
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS `{TABLE_NAME}` (
        `index` integer PRIMARY KEY,
        `ping` string DEFAULT NULL,
        `down` float DEFAULT NULL,
        `up` float DEFAULT NULL,
        `timestamp` timestamp DEFAULT NULL
        );
        ''')
    _logger.info("created SQL table")
    return conn, cursor

def print_db(DB_NAME, TABLE_NAME):
    _, cursor = connect_db(DB_NAME)
    # select all
    sql_query = f"""SELECT * FROM {TABLE_NAME} 
        """
    cursor.execute(sql_query)
    names = list(map(lambda x: x[0], cursor.description))
    res = cursor.fetchall()
    # use tabulate for prettty print
    _logger.info('db table ↓\n{}'.format(tabulate(res, headers=names)))
    temp = [x[1:] for x in res] # remove indexes
    df = pd.DataFrame(temp, columns=names[1:])
    return df