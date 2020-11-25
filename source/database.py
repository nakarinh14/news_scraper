import psycopg2
from psycopg2 import IntegrityError
import psycopg2.extras
import psycopg2.pool
import sys
# import testenv
from .env import init_env
import os

# Connect to postgres DB
init_env()
def init_conn():
    conn = psycopg2.connect(
        user = os.environ['DB_USER'],
        password = os.environ['DB_PASSWORD'],
        host = os.environ['DB_HOST'],
        port = os.environ['DB_PORT'],
        database = os.environ['DB_DATABASE']
    )
    return conn
# try:

#     pool = psycopg2.pool.SimpleConnectionPool(
#         minconn=1,
#         maxconn=20,
#         user = os.environ['DB_USER'],
#         password = os.environ['DB_PASSWORD'],
#         host = os.environ['DB_HOST'],
#         port = os.environ['DB_PORT'],
#         database = os.environ['DB_DATABASE']
#     )
#     conn = pool.getconn()
#     cur = conn.cursor()
# except:
#     print(sys.exc_info()[0])
    
        
def insert_batch(query, values: list):
    try:
        if len(values) > 0:
            conn = init_conn()
            cur = conn.cursor()
            psycopg2.extras.execute_batch(cur, query, values)
            conn.commit()
            print("Data inserted sucessfully")
        else:
            print("No data to insert")

    except IntegrityError:
        print("Duplicated URL met on DB... Shouldn't happen... Check Scraper API")
    
    # def insert_all(self, query, data):

def insert(query: str, data):
    try:
        conn = init_conn()
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
        print("Data inserted sucessfully")
        
    except IntegrityError:
        print("Duplicated URL met on DB... Shouldn't happen... Check Scraper API")

def findLatestUrl(query: str, values: list):
    try:
        conn = init_conn()
        cur = conn.cursor()
        cur.execute(query, values)
        result = cur.fetchone()
        return result[0] if result is not None else result
    except:
        print(sys.exc_info()[0])
        return None


# if __name__ == "__main__":
#     insert("INSERT INTO users (username, password) VALUES (%s, %s)", ["test", "test"])