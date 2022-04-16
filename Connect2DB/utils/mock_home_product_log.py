from database.pool import *
import sys
import random
import string
import psycopg2
import pandas as pd
from random import randrange
from datetime import timedelta
from datetime import datetime
sys.path.insert(1, './project/database')


def mock_table_view_each_cat(category_id):

    # add a mock data
    data = prepare_mocked_data(category_id)
    amountOfInteraction = random.randint(1, 10)

    conn = None
    try:
        conn = getConn()

        cur = conn.cursor()

        for i in range(amountOfInteraction):
            cur.execute(
                "INSERT INTO home_product_log(customer_id, product_id, view_date) VALUES({},{},'{}');".format(data[0], random.choice(data[1]), data[2]))
            conn.commit()

        # cur.execute("SELECT * FROM home_product_log;")
        # home_product_log_table = cur.fetchall()
        # result = list(home_product_log_table)
        # df = pd.DataFrame(result)
        # print(df)

        print("Successfully inserted user_interaction for {} times".format(
            amountOfInteraction))

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.\n')
            print("_______________________________________________________________________________________________\n")


def add_customer(customer_id):
    conn = None
    try:
        conn = getConn()

        cur = conn.cursor()

        email = ''.join(random.choice(string.ascii_letters)
                        for _ in range(7)) + "@gmail.com"
        password = "123456"
        time = datetime.now()

        cur.execute("INSERT INTO customer(id, email, password, date) VALUES({},'{}','{}','{}')".format(
            customer_id, email, password, time))
        conn.commit()

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("Successfully added the customer")
            print('Database connection closed.\n')
            print("_______________________________________________________________________________________________\n")


def prepare_mocked_data(category_id):
    # let mock user has only in range of 1 to 1000
    # based on category - in range of 100 per preference
    customer_id = random_customer_id_based_on_category_preference(category_id)
    product_id = random_product_each_cat(category_id)  # list

    # random datetime
    d1 = datetime.strptime('1/1/2020 12:00 AM', '%m/%d/%Y %I:%M %p')
    d2 = datetime.strptime('12/1/2021 12:00 AM', '%m/%d/%Y %I:%M %p')
    randomDate = random_date(d1, d2)

    # create list to collect data
    data = [customer_id, product_id, randomDate]

    return data


def random_product_each_cat(category_id):
    conn = None

    try:
        conn = getConn()

        cur = conn.cursor()

        cur.execute(
            "SELECT id, title, category_id FROM product WHERE category_id = {} ORDER BY id;".format(category_id))
        result = list(cur.fetchall())
        product_cat = pd.DataFrame(
            result, columns=["product_id", "title", "category_id"])
        #print("\n", product_cat)

        # Random element from list
        product_id_index_list = list(product_cat['product_id'].values)
        random_num = []
        random_num.append(random.choice(product_id_index_list))
        random_num.append(random.choice(product_id_index_list))
        random_num.append(random.choice(product_id_index_list))
        print("Random product_id is : {}, {}, {}\n".format(
            random_num[0], random_num[1], random_num[2]))

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.\n')
            print("_______________________________________________________________________________________________\n")
    # สุ่ม product จาก category id
    return random_num


def random_customer_id_based_on_category_preference(category_id):
    customer_id = 0
    if(category_id == 1):
        customer_id = random.randint(1, 100)
    elif(category_id == 2):
        customer_id = random.randint(101, 200)
    elif(category_id == 3):
        customer_id = random.randint(201, 300)
    elif(category_id == 4):
        customer_id = random.randint(301, 400)
    elif(category_id == 5):
        customer_id = random.randint(401, 500)
    elif(category_id == 6):
        customer_id = random.randint(501, 600)
    elif(category_id == 7):
        customer_id = random.randint(601, 700)
    elif(category_id == 8):
        customer_id = random.randint(701, 800)
    elif(category_id == 9):
        customer_id = random.randint(801, 900)
    elif(category_id == 10):
        customer_id = random.randint(901, 1000)
    print("Random customer_id is : {}\n".format(customer_id))
    return customer_id


def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)
