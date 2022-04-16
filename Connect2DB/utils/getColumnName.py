import pandas as pd
from database.pool import *
import sys
import psycopg2
sys.path.insert(1, './project/database')


def get_column_name(table_name):
    list_col = []
    conn = None
    try:
        conn = getConn() #เปิด connection
        cur = conn.cursor() #run query

        cur.execute(
            "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{}';".format(table_name))
        column_name = list(cur.fetchall())

        for i in range(0, len(column_name)):
            list_col.append(column_name[i][0])
        # print(list_col)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Blahhhh", error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.\n')
            print("_______________________________________________________________________________________________\n")

    return list_col


def column_name_to_string(list_col):
    str_col = ""
    for i in range(len(list_col)):
        if(i == 0):
            str_col = str_col + list_col[i] + ", "
        elif(1 <= i <= len(list_col)-2):
            str_col = str_col + list_col[i] + ", "
        else:
            str_col = str_col + list_col[i]
    return str_col
