import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scriptDB as sc
import sys
#from pandas_schema.validation import CustomElementValidation
#from pandas_schema import Column

from sklearn import model_selection
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, mean_squared_error, mean_absolute_error
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler

# %matplotlib inline
#plt.style.use("ggplot")

import sklearn
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import MinMaxScaler
from sklearn import model_selection
sys.setrecursionlimit(200000)
dataset = sc.data_suggest_homepage()

def setmodel():
    #print(dataset)
    ratings_utility_matrix = dataset.pivot_table(values='user_score', index='user_id', columns='product_id', fill_value=0)

    X = ratings_utility_matrix.T
    #print(X)
    popular_products = pd.DataFrame(dataset.groupby('user_id')['product_id'].sum())
    most_popular = popular_products.sort_values('product_id', ascending=False)
    SVD = TruncatedSVD(n_components=10)
    decomposed_matrix = SVD.fit_transform(X)

    return most_popular, X, decomposed_matrix

def suggestmain(userid, mostpo, Xtab, decom):
    try:
        global userbuy
        userbuy = dataset.loc[dataset['user_id']==userid,['product_id']]
        productbase=userbuy.loc[userbuy.index[0],'product_id']
        print("productbase")
        print(productbase)
        product_names = list(Xtab.index)
        product_ID = product_names.index(productbase)
        correlation_matrix = np.corrcoef(decom)
        correlation_product_ID = correlation_matrix[product_ID]

        #corr_product = {}
        #for id in products:
            #corr_product[id] = corr

        #Recommend = list(Xtab.index[correlation_product_ID>0])
        #Recommend.remove(productbase)
        Recom = []
        for x in range(100, -100, -1):
            Recom.extend(list(Xtab.index[((x+1)/100)>=correlation_product_ID>=(x/100)]))
        Recom.remove(productbase)
        sc.insert_data_suggestionHomepage(userid, Recom[:120])
        #print(Recom[:120])
        return (Recom[:120])
    except:
        suggest = mostpo['product_id'].values.tolist()
        sc.insert_data_suggestionHomepage(userid, suggest)
        print(suggest[:120])
        return suggest[:120]

def newusersuggestion(mostpo):
    popular = mostpo['product_id'].values.tolist()
    #print(popular)
    return popular[:120]


##Pice model
def preparing_data():
    query = sc.query_for_suggest_homepage()
    df = pd.DataFrame(query, columns = ['user_id','product_id','interaction_score','price', 'category_code'])
    #df = pd.read_csv('./csv/Result_10.csv')
    print("df")
    #print(df['price'].describe())
    df['price_category'] = 0
    #for i in df['category_code'].unique():
    #for i in range (1,12):
    #df.loc[df['category_code'] == i, 'price_category'] = pd.qcut(x=df['price'][df['category_code'] == i],q=5,labels=[1, 2, 3, 4, 5])
        #print(i)
    df['price_category'] = 0
    for j in range (1, 10):
        a = df.loc[df['category_code']==j, 'price']
        a = pd.DataFrame(a)
        keep = a.sort_values(by='price', inplace=True)
        price_unique = pd.unique(a['price'])

        price_sorted = a.values
        #print(price_sorted[0][0])
        a = a.index
        k = 1
        first = price_unique[int(len(price_unique)*.2)]
        second = price_unique[int(len(price_unique) * .4)]
        third = price_unique[int(len(price_unique) * .6)]
        fourth = price_unique[int(len(price_unique) * .8)]

        for i in range (0, len(a)):
            if price_sorted[i][0] > fourth:
                df.loc[a[i], 'price_category'] = 5
            elif price_sorted[i][0]>third:
                df.loc[a[i], 'price_category'] = 4
            elif price_sorted[i][0] > second:
                df.loc[a[i], 'price_category'] = 3
            elif price_sorted[i][0] >first:
                df.loc[a[i], 'price_category'] = 2
            else:
                df.loc[a[i], 'price_category'] = 1
        '''for i in range (len(a)-1,-1,-1):
            if(i > (len(a)*.8)+1) :
                k = 5
            elif i > (len(a)*.6) +1:
                k = 4
            elif i > (((len(a)) * .4))+1:
                k = 3
            elif i > (((len(a)) * .2))-1:
                k = 2
            df.loc[a[i],'price_category'] = k'''
        '''new = (np.array_split(a, 5))
        for i in range (1, 6):
            for m in range(0, new[i-1].size):
                df.loc[new[i-1][m], 'price_category'] = i
        print(new[0].size)'''
    group  = df.copy()
    group.rename({'interaction_score': 'user_score'}, axis=1, inplace=True)

    for i in range(len(group)):
        if group['category_code'][i] == 1:
            group['category_code'][i] = "computer & mobile"
        elif group['category_code'][i] == 2:
            group['category_code'][i] = "education"
        elif group['category_code'][i] == 3:
            group['category_code'][i] = "fashion"
        elif group['category_code'][i] == 4:
            group['category_code'][i] = "beauty"
        elif group['category_code'][i] == 5:
            group['category_code'][i] = "furniture"
        elif group['category_code'][i] == 6:
            group['category_code'][i] = "electronics"
        elif group['category_code'][i] == 7:
            group['category_code'][i] = "food"
        elif group['category_code'][i] == 8:
            group['category_code'][i] = "sports"
        elif group['category_code'][i] == 9:
            group['category_code'][i] = "accessories"

    group['user_score'] = group['user_score'].apply(lambda x: 100 if x > 100 else x)

    std = MinMaxScaler(feature_range=(0.025, 1))
    std.fit(group['user_score'].values.reshape(-1, 1))
    group['interaction_score'] = std.transform(group['user_score'].values.reshape(-1, 1))

    return group

def model_implementation(group):
    X_train_val, X_test = model_selection.train_test_split(group, test_size=0.2, random_state=42)
    X_train, X_valid = model_selection.train_test_split(X_train_val, test_size=0.16, random_state=42)

    X_train_matrix = pd.pivot_table(X_train, values='user_score', index='user_id', columns='product_id')
    X_train_matrix = X_train_matrix.fillna(0)
    #print("Xtrainmatrix " + str(X_train_matrix.shape))
    # get uniqu product dataframe
    unique_product = np.unique(np.array(group['product_id']))
    group_pro = group[['product_id', 'price_category', 'category_code']]
    #print("GroupproDup " + str(group_pro.shape))
    group_pro = group_pro.drop_duplicates()
    #print(group_pro)
    #print("Grouppro " + str(group_pro.shape))
    # get product_id from X_train_matrix only
    group_pro_index_df = group_pro.set_index('product_id')
    product_cat = group_pro_index_df.loc[list(X_train_matrix.columns), :]
    product_cat.reset_index(inplace=True)
    #print("Product Cat " + str(product_cat.shape))
    price_cat_matrix = np.reciprocal(euclidean_distances(np.array(product_cat['price_category']).reshape(-1, 1)) + 1)
    euclidean_matrix = pd.DataFrame(price_cat_matrix, columns=product_cat['product_id'],
                                    index=product_cat['product_id'])
    #print("Euclidian " + str(euclidean_matrix.shape))
    tfidf_vectorizer = TfidfVectorizer()
    doc_term = tfidf_vectorizer.fit_transform(list(product_cat['category_code']))  # vector of dictionary in document
    dt_matrix = pd.DataFrame(doc_term.toarray().round(3), index=[i for i in product_cat['product_id']],
                             columns=tfidf_vectorizer.get_feature_names())
    cos_similar_matrix = pd.DataFrame(cosine_similarity(dt_matrix.values), columns=product_cat['product_id'],
                                      index=product_cat['product_id'])
    #print("Cos similarity " + str(cos_similar_matrix.shape))
    similarity_matrix = cos_similar_matrix.multiply(euclidean_matrix)
    content_matrix = X_train_matrix.dot(similarity_matrix)

    std = MinMaxScaler(feature_range=(0, 1))
    std.fit(content_matrix.values)
    content_matrix = std.transform(content_matrix.values)

    content_matrix = pd.DataFrame(content_matrix, columns=sorted(X_train['product_id'].unique()),
                                  index=sorted(X_train['user_id'].unique()))
    content_df = content_matrix.stack().reset_index()
    content_df = content_df.rename(columns={'level_0': 'user_id', 'level_1': 'product_id', 0: 'predicted_interaction'})
    X_valid = X_valid.merge(content_df, on=['user_id', 'product_id'])
    #print(content_matrix)
    X_valid['predicted_purchase'] = X_valid['predicted_interaction'].apply(lambda x: 1 if x >= 0.5 else 0)

    return content_df

def predict_homepage(content_df, uid):
    customer = content_df[content_df['user_id'] == int(uid)]
    customer.sort_values(by=['predicted_interaction'], ascending=False, inplace=True)
    print("uid")
    print(uid)
    products = customer['product_id'][:140].sample(frac=1).values.tolist()[:120]
    if len(products) == 0:
       products = find_hit_homepage()
    sc.insert_data_suggestionHomepage(uid, products)
    print(type(products))
    return products

def find_hit_homepage ():
    df = sc.query_most_interaction_product()
    df = pd.DataFrame(df, columns=['product_id', 'score'])
    products = df['product_id'][:160].sample(frac=1)
    return products[:120].values.tolist()