import pandas as pd
from database.pool import *
import sys
import psycopg2
sys.path.insert(1, './project/database')


def get_search_dataframe():

    conn = None
    try:
        conn = getConn()
        cur = conn.cursor()

        cur.execute("SELECT id, title, category_id FROM product")
        result = list(cur.fetchall())
        df = pd.DataFrame(result, columns=["id", "title", "category_id"])

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Blahhhh", error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.\n')
            print("_______________________________________________________________________________________________\n")

    return df
