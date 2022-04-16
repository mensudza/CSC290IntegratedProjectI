#import os
from database.config import config
import psycopg2
from psycopg2 import pool
# import sys
# sys.path.append('/.../project/database')

postgreSQL_pool = None
params = None


def initPool():

    global postgreSQL_pool
    global params

    try:
        #BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        params = config()
        postgreSQL_pool = pool.SimpleConnectionPool(1, 1000, user=params["user"],
                                                    password=params["password"],
                                                    host=params["host"],
                                                    port=params["port"],
                                                    database=params["database"])
        if (postgreSQL_pool):
            print("\nConnection pool created successfully\n")

        # ps_connection = postgreSQL_pool.getconn()

        # if (ps_connection):
        #     print("\nsuccessfully recived connection from connection pool ")
        #     return ps_connection

        #     # Use this method to release the connection object and send back to connection pool
        #     postgreSQL_pool.putconn(ps_connection)
        #     print("Put away a PostgreSQL connection")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Blehhh Error while connecting to PostgreSQL", error)


def getConn():
    ps_connection = postgreSQL_pool.getconn()

    if(ps_connection):
        print("successfully recieved connection from connection pool\n")
        return ps_connection
    else:
        print("Can't recieved connection from connection pool\n")


def closePool():
    if postgreSQL_pool:
        postgreSQL_pool.closeall
    print("PostgreSQL connection pool is closed\n")
    print("_______________________________________________________________________________________________\n")
