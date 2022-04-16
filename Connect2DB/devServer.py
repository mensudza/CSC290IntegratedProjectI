from flask import Flask
from flask import request
import scriptDB as db
from flask_cors import CORS
import search_count
import utils.inserToRecommendationTable as insertRecTable
import suggestHomepage as suggest
import train_home

#fai
df = db.for_train_search_model()
ai_index = search_count.learn_relation_title(df, './model/keyword2vec_model.bin')

#homepage
group = suggest.preparing_data()
content_df = suggest.model_implementation(group)



app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Members API Route

@app.route("/search", methods=['GET', 'POST'])
def search():
   query = request.args.get("q")
   keyword = search_count.keyword(query)
   products = search_count.search_and_show(ai_index, query)
   print(keyword)
   return {"keyword" : query, "products" : products}


@app.route("/suggestHomepageMember", methods=['GET', 'POST'])
def suggest_homepage_member():
    userid = request.args.get("uid")
    products = suggest.predict_homepage(content_df, userid)
    print(products)
    return {"uid":userid, "products" : products}

@app.route("/suggestHomepageGeneral", methods = ['GET', 'POST'])
def suggest_homepage_general():
    products = suggest.find_hit_homepage()
    print(products)
    return {"uid": "general", "products" : products}

@app.route("/relatedProduct", methods=['GET', 'POST'])
def related_product():
    idProduct = request.args.get("id")
    title, products = search_count.find_related_product(ai_index, idProduct)
    return {"idProduct" : idProduct,
            "titleProduct" : title,
            "products" : products}


#trigger
@app.route("/train_keyword", methods=['GET', 'POST'])
def train_key():
    search_count.train_keyword()
    return {"progress" : "done"}

@app.route("/update_each_rec_score", methods=['GET', 'POST'])
def update_each_rec():
    insertRecTable.insert_rem_number_view_product()
    insertRecTable.insert_rem_number_product_in_cart()
    insertRecTable.insert_rem_number_payment_product()
    return {"progress" : "done"}

@app.route("/update_interation_score", methods=['GET', 'POST'])
def update_score():
    for i in range(1, 501):
        db.cal_interaction_score(i)
    return {"progress" : "done"}

@app.route("/train_homepage", methods=['GET', 'POST'])
def train_homepage():
    group = suggest.preparing_data()
    return {"progress": "done"}

if __name__ == "__main__":
  app.run(debug=False, host = "0.0.0.0", port = 5001)