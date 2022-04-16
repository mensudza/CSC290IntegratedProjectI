import pandas as pd
from database.pool import *
import sys
import psycopg2



sys.path.insert(1, './project/database')



def execute_update(query):

    conn = None
    try:
        conn = getConn()
        cur = conn.cursor()

        cur.execute(query)
        conn.commit()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Blahhhh", error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.\n')
            print("_______________________________________________________________________________________________\n")