import psycopg2
import sys
import pandas as pd
from database.pool import *
import sys
import psycopg2
sys.path.insert(1, './project/database')

# All of the model scripts
#from model_mayfav import *
# import utils.getColumnName as getColumnName this works too.
from database.pool import *
from utils.mock_home_product_log import *
from utils.selectTable import *
from utils.executeQuery import *
from utils.getColumnName import *
from utils.mock_home_add_to_cart_log import *
from utils.getSearchDataframe import *
from utils.executeDelete import *
from utils.executeUpdate import *

sys.path.append('./project/database')
sys.path.append('./project/utils')


def checkConnection():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        conn = getConn()

        # create a cursor
        cur = conn.cursor()
        # execute a statement & display the PostgreSQL database server version
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version, "\n")

        cur.execute('SELECT * FROM product LIMIT 10')
        result = list(cur.fetchall())
        df = pd.DataFrame(result)
        print(df)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Blahhhh", error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.\n')
            print("_______________________________________________________________________________________________\n")


#if __name__ == '__main__':
def test():
    initPool()

    # for i in range(100):
    #    mock_table_view_each_cat(category_id=1)

    # select_table("home_product_log")

    # execute_query(
    #   "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'home_product_log';")
    #a = get_column_name("home_product_log")
    # print(column_name_to_string(a))

    # for i in range(101, 1000):
    # add_customer(1000)

    df = get_search_dataframe()
    print(df)

    #execute_delete("DELETE FROM home_product_log;")

    select_table_to_dataframe(attributes=["customer_id", "product_id"],
                              table="home_product_log")

    select_table_to_dataframe(attributes=get_column_name(
        "home_add_to_cart_log"), table="home_add_to_cart_log")

    # mock_table_add_to_cart_each_cat(3)
    closePool()

    #may_fav_product_model(csvFile=raw_data_path, corr=corrdata_path)

def for_train_search_model():
    initPool()

    df = select_table_to_dataframe(attributes=["id", "title"],
                             table="product")

    #df = select_table_to_dataframe(attributes=get_column_name(
    #    "product"), table="product")

    closePool()
    return df


def insert_data(q, newcount):
    initPool()
    #execute_update("INSERT INTO rem_number_keyword_search(keyword, number_searched) VALUES ('apple', 1)")
    num = execute_query("SELECT number_searched FROM rem_number_keyword_search WHERE keyword = '{}'".format(q))
    if(len(num) == 0):
        execute_update("INSERT INTO rem_number_keyword_search(keyword, number_searched) VALUES ('{}', 1)".format(q))

    else:
        num = num[0][0] + newcount
        execute_update("UPDATE rem_number_keyword_search SET number_searched = {} WHERE keyword = '{}'".format(num,q))

    df = select_table_to_dataframe(attributes=["keyword", "number_searched"],
                                   table="rem_number_keyword_search")

    # df = select_table_to_dataframe(attributes=get_column_name(
    #    "product"), table="product")

    closePool()
    return df

def insert_data_related(idProduct, related_lists):
    initPool()
    #execute_update("INSERT INTO rem_number_keyword_search(keyword, number_searched) VALUES ('apple', 1)")
    related = execute_query("SELECT related_product FROM rem_related_products WHERE product_id = {}".format(idProduct))
    if(len(related) == 0):
        execute_update("INSERT INTO rem_related_products(product_id, related_product) VALUES ({}, ARRAY {})".format(idProduct, related_lists))

    else:
        execute_update("UPDATE rem_related_products SET related_product = ARRAY {} WHERE product_id = {}".format(related_lists, idProduct))

    df = select_table_to_dataframe(attributes=["product_id", "related_product"],
                                   table="rem_related_products")

    # df = select_table_to_dataframe(attributes=get_column_name(
    #    "product"), table="product")

    closePool()
    return df

def insert_sub_title(id_product, subtitle):
    initPool()
    execute_update("UPDATE product SET sub_title = '{}' WHERE id = {}".format(subtitle, id_product))
    closePool()

def find_title(id_product):
    initPool()
    title = execute_query("SELECT title FROM product WHERE id = {}".format(id_product))
    print(title[0][0])
    closePool()
    return title[0][0]

def cal_interaction_score(uid):
    initPool()
    view = execute_query(
        "SELECT product_id, sum(total_view) as view FROM rem_number_view_product WHERE customer_id = {} GROUP BY product_id ORDER BY view desc".format(uid))

    cart = execute_query(
        "SELECT product_id, sum(sum_in_cart) as cart FROM rem_number_product_in_cart WHERE customer_id = {} GROUP BY product_id ORDER BY cart desc".format(
            uid))
    purchase = execute_query(
        "SELECT product_id, sum(sum_buy) as buy FROM rem_number_payment_product WHERE customer_id = {} GROUP BY product_id ORDER BY buy desc".format(
            uid))
    print(view) #1
    print(cart) #10
    print(purchase) #50
    interaction_score = {}
    for i in range (0,len(view)):
        try:
            interaction_score[view[i][0]] = view[i][1]
        except KeyError:
            interaction_score[view[i][0]] = view[i][1]

    for i in range (0, len(cart)):
        try:
            interaction_score[cart[i][0]] += (cart[i][1] * 10)
        except:
            interaction_score[cart[i][0]] = cart[i][1]*10

    for i in range (0, len(purchase)):
        try:
            interaction_score[purchase[i][0]] += (purchase[i][1]*50)
        except:
            interaction_score[purchase[i][0]] = purchase[i][1] * 50

    print(interaction_score)

    for pid in interaction_score.keys():
        exist_id = execute_query(
            "SELECT interaction_score FROM rem_number_interaction_user WHERE customer_id = {} and product_id = {}".format(uid, pid))
        #print(len(exist_id))
        #print(pid)
        if (len(exist_id) == 0):
            execute_update(
                "INSERT INTO rem_number_interaction_user(customer_id, product_id, interaction_score) VALUES ({}, {}, {})".format(uid,pid,interaction_score[pid]))

        else:
            execute_update(
                "UPDATE rem_number_interaction_user SET interaction_score = {} WHERE product_id = {} and customer_id = {}".format(interaction_score[pid],pid,uid))

    closePool()

def data_suggest_homepage():
    initPool()
    df = execute_query("SELECT customer_id, product_id, interaction_score FROM rem_number_interaction_user")
    df = pd.DataFrame(df, columns=['user_id', 'product_id', 'user_score'])
    closePool()
    return df

def insert_data_suggestionHomepage(uid, products_lists):
    initPool()
    #execute_update("INSERT INTO rem_number_keyword_search(keyword, number_searched) VALUES ('apple', 1)")
    print(uid)
    products = execute_query("SELECT product_id FROM rem_suggestion_homepage WHERE customer_id = {}".format(uid))
    if(len(products) == 0):
        execute_update("INSERT INTO rem_suggestion_homepage(customer_id, product_id) VALUES ({}, ARRAY {})".format(uid, products_lists))

    else:
        execute_update("UPDATE rem_suggestion_homepage SET product_id = ARRAY {} WHERE customer_id = {}".format(products_lists, uid))

    df = select_table_to_dataframe(attributes=["customer_id", "products_id"],
                                   table="rem_suggestion_homepage")

    # df = select_table_to_dataframe(attributes=get_column_name(
    #    "product"), table="product")

    closePool()
    return df

def query_for_suggest_homepage():
    initPool()
    df = execute_query("select customer_id as user_id, product_id, interaction_score, price, category_id as category_code from cshop.public.rem_number_interaction_user as r_in INNER JOIN cshop.public.product as pro ON pro.id = r_in.product_id order by customer_id, product_id")
    closePool()
    return df

def query_most_interaction_product():
    initPool()
    df = execute_query("select product_id, sum(interaction_score) as total from rem_number_interaction_user group by product_id order by total desc")
    closePool()
    return df

"""DB_HOST = "db1.cshop.cscms.ml"
DB_NAME = "cshop-ml"
DB_USER = "cs21"
DB_PASS = "cs212021"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                        password=DB_PASS, host=DB_HOST, port=5431)

cur = conn.cursor()

# cur.execute(
#   "INSERT INTO event(id, title, description) VALUES (1, 'General', 'Transaction in general');")
# conn.commit()

#cur.execute("INSERT INTO rem_number_view_product(customer_id, product_id, total_view, event_id, added_time) VALUES (1,10, 12, 1, '2021-05-07');")
# conn.commit()

#sql1 = "SELECT * FROM rem_number_view_product;"
#cur.execute(sql1)
#print(cur.fetchall())

sql2 = "SELECT * FROM product;"
cur.execute(sql2)
print(cur.fetchone())


cur.close()

conn.close()"""
