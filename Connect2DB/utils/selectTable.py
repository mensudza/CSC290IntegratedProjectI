import pandas as pd
from database.pool import *
import sys
import psycopg2
from utils.getColumnName import *
sys.path.insert(1, './project/database')

# attributes -> list


def select_table_to_dataframe(attributes, table):

    conn = None
    df = pd.DataFrame([])
    try:
        conn = getConn()
        cur = conn.cursor()

        cur.execute('SELECT {} FROM {}'.format(
            column_name_to_string(attributes), table))
        result = list(cur.fetchall())
        df = pd.DataFrame(result, columns=attributes)
        #print(df)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Blahhhh", error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.\n')
            print("_______________________________________________________________________________________________\n")
    return df