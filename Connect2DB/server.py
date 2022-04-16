from flask import Flask
from flask import request
import scriptDB as db
from flask_cors import CORS
import search_count

df = db.for_train_search_model()
ai_index = search_count.learn_relation_title(df, './model/keyword2vec_model.bin')

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


@app.route("/suggestHomepage", methods=['GET', 'POST'])
def suggest_homepage():
    userid = request.args.get("uid")
    return {"uid":userid, "products" : ["no1","no2"]}


@app.route("/relatedProduct", methods=['GET', 'POST'])
def related_product():
    idProduct = request.args.get("id")
    title, products = search_count.find_related_product(ai_index, idProduct)
    return {"idProduct" : idProduct,
            "titleProduct" : title,
            "products" : products}


if __name__ == "__main__":
    app.run(debug=False, host = "0.0.0.0", port = 5002)


'''from flask import Flask

#import search_count as search
from flask import request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Members API Route

@app.route("/search", methods=['GET', 'POST'])
def search():
    query = request.args.get("q")
    return {"keyword" : query,
            "products" : [
            15417,
            13843,
            20027,
            13462,
            13792,
            13385,
            20078,
            25590,
            25181,
            25216,
            25631,
            25543,
            19654,
            2141,
            18845,
            23651,
            2391,
            19774,
            19365,
            643,
            1978,
            812,
            1728,
            1311,
            210,
            1061,
            116,
            18969,
            361,
            1206,
            519,
            19247,
            24448,
            1571,
            25126,
            943,
            24977,
            25392,
            354,
            24949,
            23576,
            25447,
            1929,
            2347,
            21009,
            25027,
            25592,
            1520]}


@app.route("/suggestHomepage", methods=['GET', 'POST'])
def suggest_homepage():
    userid = request.args.get("uid")
    return {"uid": userid
            , "products":[
            15417,
            13843,
            20027,
            13462,
            13792,
            13385,
            20078,
            25590,
            25181,
            25216,
            25631,
            25543,
            19654,
            2141,
            18845,
            23651,
            2391,
            19774,
            19365,
            643,
            1978,
            812,
            1728,
            1311,
            210,
            1061,
            116,
            18969,
            361,
            1206,
            519,
            19247,
            24448,
            1571,
            25126,
            943,
            24977,
            25392,
            354,
            24949,
            23576,
            25447,
            1929,
            2347,
            21009,
            25027,
            25592,
            1520]}

@app.route("/relatedProduct", methods=['GET', 'POST'])
def related_product():
    idProduct = request.args.get("id")
    titleProduct = request.args.get("title")
    return {"idProduct" : idProduct,
                "title" : titleProduct,
            "products" : [15417,
            13843,
            20027,
            13462,
            13792,
            13385,
            20078,
            25590,
            25181,
            25216,
            25631,
            25543,
            19654,
            2141,
            18845,
            23651,
            2391,
            19774,
            19365,
            643,
            1978,
            812,
            1728,
            1311,
            210,
            1061,
            116,
            18969,
            361,
            1206,
            519,
            19247,
            24448,
            1571,
            25126,
            943,
            24977,
            25392,
            354,
            24949,
            23576,
            25447,
            1929,
            2347,
            21009,
            25027,
            25592,
            1520]}


if __name__ == "__main__":
    app.run(debug=False, host = "0.0.0.0", port = 5001)
'''