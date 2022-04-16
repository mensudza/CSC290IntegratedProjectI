import pandas as pd
from database.pool import *
import sys
import psycopg2
sys.path.insert(1, './project/database')


def execute_query(query):
    conn = None
    df = pd.DataFrame([])
    try:
        conn = getConn()
        cur = conn.cursor()

        cur.execute(query)
        df = cur.fetchall()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Blahhhh", error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.\n')
            print("_______________________________________________________________________________________________\n")
        return df