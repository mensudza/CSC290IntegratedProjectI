from database.pool import *
import sys
import pandas as pd
import numpy as np
import random
import psycopg2
from random import randrange
from datetime import datetime
from utils.getColumnName import *
sys.path.insert(1, './project/database')


def insert_rem_number_view_product():
    conn = None
    try:
        conn = getConn()
        cur = conn.cursor()

        added_time = datetime.now()
        event_id = 1

        sql = """SELECT customer_id, product_id, count(*)
                FROM cshop.public.home_product_log
                GROUP BY customer_id, product_id
                ORDER BY customer_id;"""

        cur.execute(sql)
        result = list(cur.fetchall())

        attr_str = "customer_id, product_id, total_view, event_id, added_time"

        for i in result:
            customer_id = i[0]
            product_id = i[1]
            total_view = i[2]

            if(id_check(customer_id, product_id, "rem_number_view_product") == 0):
                cur.execute("INSERT INTO rem_number_view_product({}) VALUES({}, {}, {}, '{}', {});".format(
                    attr_str, customer_id, product_id, total_view, event_id, added_time))
                conn.commit()
                print("Inserted rem_number_view_product(customer_id : {}, product_id : {}".format(
                    customer_id, product_id))
            else:
                sql_update = """UPDATE rem_number_view_product
                                SET total_view = {}
                                WHERE customer_id = {} AND product_id = {};""".format(total_view, customer_id, product_id)
                cur.execute(sql_update)
                conn.commit()
                print("Updated rem_number_view_product(customer_id : {}, product_id : {}".format(
                    customer_id, product_id))

        print("\ninserted rem_number_view_product completed\n")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Blahhhh", error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.\n')
            print("_______________________________________________________________________________________________\n")


def insert_rem_number_product_in_cart():
    conn = None
    try:
        conn = getConn()
        cur = conn.cursor()

        added_time = datetime.now()
        event_id = 1

        sql = """select customer_id, product_id, count(*)
                from cshop.public.home_add_to_cart_log
                group by customer_id, product_id
                order by customer_id;"""
        cur.execute(sql)
        result = list(cur.fetchall())

        attr_str = "customer_id, product_id, sum_in_cart, added_time, event_id"

        for i in result:
            customer_id = i[0]
            product_id = i[1]
            sum_in_cart = i[2]

            if(id_check(customer_id, product_id, "rem_number_product_in_cart") == 0):
                cur.execute("INSERT INTO rem_number_product_in_cart({}) VALUES({}, {}, {}, '{}', {});".format(
                    attr_str, customer_id, product_id, sum_in_cart, added_time, event_id))
                conn.commit()
                print("Inserted rem_number_product_in_cart(customer_id : {}, product_id : {}".format(
                    customer_id, product_id))
            else:
                sql_update = """UPDATE rem_number_product_in_cart
                                SET sum_in_cart = {}
                                WHERE customer_id = {} AND product_id = {};""".format(sum_in_cart, customer_id, product_id)
                cur.execute(sql_update)
                conn.commit()
                print("Updated rem_number_product_in_cart(customer_id : {}, product_id : {}".format(
                    customer_id, product_id))

        print("\ninserted rem_number_product_in_cart completed\n")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Blahhhh", error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.\n')
            print("_______________________________________________________________________________________________\n")


def insert_rem_number_payment_product():
    conn = None
    try:
        conn = getConn()
        cur = conn.cursor()

        added_time = datetime.now()
        event_id = 1

        sql = """with order_grouped_but_not_sum(customer_id, product_id, quantity, price) as
                    (select customer_id, product_id, quantity, price
                    from cshop.public."order" INNER JOIN order_item
                    on "order".id = order_item.order_id)
                select customer_id, product_id, sum(quantity) as quantity, sum(price) as sum_price
                from order_grouped_but_not_sum
                group by customer_id, product_id
                order by customer_id;"""
        cur.execute(sql)
        result = list(cur.fetchall())

        attr_str = "customer_id, product_id, sum_buy, added_time, event_id"

        for i in result:
            customer_id = i[0]
            product_id = i[1]
            sum_buy = i[2]

            if(id_check(customer_id, product_id, "rem_number_payment_product") == 0):
                cur.execute("INSERT INTO rem_number_payment_product({}) VALUES({}, {}, {}, '{}', {});".format(
                    attr_str, customer_id, product_id, sum_buy, added_time, event_id))
                conn.commit()
                print("Inserted rem_number_payment_product(customer_id : {}, product_id : {}".format(
                    customer_id, product_id))
            else:
                sql_update = """UPDATE rem_number_payment_product
                                SET sum_buy = {}
                                WHERE customer_id = {} AND product_id = {};""".format(sum_buy, customer_id, product_id)
                cur.execute(sql_update)
                conn.commit()
                print("Updated rem_number_payment_product(customer_id : {}, product_id : {}".format(
                    customer_id, product_id))

        print("\ninserted rem_number_payment_product completed\n")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Blahhhh", error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.\n')
            print("_______________________________________________________________________________________________\n")


def insert_rem_number_interaction_user():
    conn = None
    try:
        conn = getConn()
        cur = conn.cursor()

        customer_product_lst = get_all_customer_product_involved()

        for i in customer_product_lst:
            customer_id = i[0]
            product_id = i[1]

            cur.execute("")

        # sql = ""
        # cur.execute(sql)
        # result = list(cur.fetchall())

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Blahhhh", error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.\n')
            print("_______________________________________________________________________________________________\n")


def id_check(customer_id, product_id, table_check):
    conn = None
    try:
        conn = getConn()
        cur = conn.cursor()
        sql = """SELECT *
                FROM {}
                WHERE customer_id = {} AND product_id = {};""".format(table_check, customer_id, product_id)
        cur.execute(sql)
        result = list(cur.fetchall())
        df = pd.DataFrame(result)
        # if len(df) = 0, it means there is no (customer_id, product_id) in rem_payment_product table
        print(len(df))

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Blahhhh", error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.\n')
            print("_______________________________________________________________________________________________\n")

    return len(df)


def get_all_customer_product_involved():
    conn = None
    try:
        conn = getConn()
        cur = conn.cursor()

        sql = "SELECT customer_id, product_id FROM rem_number_view_product"
        cur.execute(sql)
        result = list(cur.fetchall())
        #print(result[0], len(result))

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Blahhhh", error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.\n')
            print("_______________________________________________________________________________________________\n")

    return result
