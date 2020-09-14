from typing import Tuple

import psycopg2
from psycopg2.extensions import connection,cursor

#defaults
DB_HOST = "127.0.0.1"
DB_NAME = "sparkifydb"
DB_USER = "student"
DB_PASSWORD = "student"

def get_connection(db: str=None,user="student",password="student") -> Tuple[connection, cursor]:
    """connect to database and return a connection and cursor tuple"""
    if not db:
        db = DB_NAME
    try:
        conn = psycopg2.connect(f"host={DB_HOST} dbname={db} user={user} password={password}")
        conn.set_session(autocommit=True)
        curr = conn.cursor()
        return conn, curr
    except psycopg2.OperationalError as e:
        if str(e).find("Connection refused")>0:
            print("Error: could not connect to postgresql server!!")
        elif str(e).find('\"'+db+'\"'):
            print("The database",db,"does not exist.")

    

