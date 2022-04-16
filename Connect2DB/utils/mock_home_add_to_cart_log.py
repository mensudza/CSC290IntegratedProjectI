from database.pool import *
import sys
import pandas as pd
import numpy as np
import random
import psycopg2
from random import randrange
from datetime import timedelta
from datetime import datetime
from utils.getColumnName import *
sys.path.insert(1, './project/database')


def mock_table_add_to_cart_each_cat(user_id):
    amount = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    distribution = [0.25, 0.25, 0.10, 0.10, 0.10, 0.07, 0.07, 0.03, 0.02, 0.01]
    conn = None
    try:
        conn = getConn()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM home_product_log WHERE customer_id={} ORDER BY product_id".format(user_id))
        result = list(cur.fetchall())
        df_view = pd.DataFrame(
            data=result, columns=get_column_name("home_product_log"))
        print(df_view)

        total_product = df_view['product_id'].values
        unique_product = np.unique(np.array(total_product))
        unique_product = list(unique_product)
        print(unique_product)

        d1 = datetime.strptime('1/1/2020 12:00 AM', '%m/%d/%Y %I:%M %p')
        d2 = datetime.strptime('12/1/2021 12:00 AM', '%m/%d/%Y %I:%M %p')
        randomDate = random_date(d1, d2)

        random_cart_amount = np.random.choice(np.array(amount), p=distribution)
        for i in range(1, random_cart_amount):
            cur.execute("INSERT INTO home_add_to_cart_log({}) VALUES({}, {}, {})".format(
                column_name_to_string("home_add_to_cart_log"), user_id, random.choice(unique_product), randomDate))
            conn.commit()

        print("successfully added to cart!!")

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.\n')
            print("_______________________________________________________________________________________________\n")


def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)
