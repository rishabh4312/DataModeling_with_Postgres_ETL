from psycopg2.extensions import connection,cursor
from db import get_connection
from sql_queries import create_table_queries,drop_table_queries


def create_database(defaultDB='student') -> None:
    #connect to default database
    conn,curr = get_connection(db=defaultDB)

    #create sparkify database with UTF8 encoding
    curr.execute("DROP DATABASE IF EXISTS sparkifydb")
    curr.execute("CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0")

    #close connection to default database
    conn.close()
    curr.close()

def drop_tables(cur: cursor,conn: connection) -> None:
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()
    
def create_tables(cur: cursor,con: connection) -> None:
    conn,cur = get_connection()
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()

def main():

    #CREATE A DATABASE sporkifydb
    create_database()

    #GET CONNECTION AND CURSOR
    conn,curr = get_connection()
    
    #CREATE TABLES
    drop_tables(curr,conn)
    create_tables(curr,conn)

    # CLOSE CONNECTION TO DATABASE
    curr.close()
    conn.close()

if __name__ ==  "__main__":

    main() #calling main method
    print("successfully created tables!!")