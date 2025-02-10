from init import *
from icecream import ic
import sqlite3
from sqlite3 import Error
from datetime import datetime


def time_format ():
    return f'{datetime.now()}  data acq|> '


ic.configureOutput(prefix=time_format)


def create_connection (db_file=db_name):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        pp = ('Conected to version: ' + sqlite3.version)
        ic(pp)
        return conn
    except Error as e:
        ic(e)

    return conn


def create_table (conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        ic(e)


def init_db (database=db_name):
    tables = [
        """ CREATE TABLE IF NOT EXISTS `data` (
	`name`	TEXT NOT NULL,
	`timestamp`	TEXT NOT NULL,
	`value`	TEXT NOT NULL,
	FOREIGN KEY(`value`) REFERENCES `iot_devices`(`name`)
    );""",
        """CREATE TABLE IF NOT EXISTS `iot_devices` (
	`sys_id`	INTEGER PRIMARY KEY,
	`name`	TEXT NOT NULL UNIQUE,
	`status`	TEXT,
	`last_updated`	TEXT NOT NULL,
	`machine`	TEXT,
	`dev_type`	TEXT NOT NULL,
	`dev_pub_topic`	TEXT,
    `dev_sub_topic`	TEXT		
    ); """
    ]
    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create tables
        for table in tables:
            create_table(conn, table)
        conn.close()
    else:
        ic("Error! cannot create the database connection.")


def create_IOT_dev (name, status, last_updated, machine, dev_type, dev_pub_topic, dev_sub_topic):
    """
    Create a new IOT device into the iot_devices table
    :param conn:
    :param :
    :return: sys_id
    """
    sql = ''' INSERT INTO iot_devices(name, status, last_updated, machine, dev_type, dev_pub_topic, dev_sub_topic)
              VALUES(?,?,?,?,?,?,?) '''
    conn = create_connection()
    if conn is not None:
        cur = conn.cursor()
        cur.execute(sql, [name, status, last_updated, machine, dev_type, dev_pub_topic, dev_sub_topic])
        conn.commit()
        re = cur.lastrowid
        conn.close()
        return re
    else:
        ic("Error! cannot create the database connection.")

def timestamp():
    return str(datetime.fromtimestamp(datetime.timestamp(datetime.now()))).split('.')[0]

def add_IOT_data(name, updated, value):
    """
    Add new IOT device data into the data table
    :param conn:
    :param :
    :return: last row id
    """
    sql = ''' INSERT INTO data(name, timestamp, value)
              VALUES(?,?,?) '''
    conn = create_connection()
    if conn is not None:
        cur = conn.cursor()
        cur.execute(sql, [name, updated, value])
        conn.commit()
        re = cur.lastrowid
        conn.close()
        return re
    else:
        ic("Error! cannot create the database connection.")


def read_IOT_data (table, name):
    """
    Query tasks by name
    :param conn: the Connection object
    :param name:
    :return: selected by name rows list
    """

    conn = create_connection()
    if conn is not None:
        cur = conn.cursor()
        cur.execute("SELECT * FROM " + table + " WHERE name=?", (name,))
        rows = cur.fetchall()
        return rows
    else:
        ic("Error! cannot create the database connection.")