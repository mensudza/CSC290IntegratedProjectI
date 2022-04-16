import scriptDB as sc
import utils.executeUpdate as update
import utils.selectTable as select
import utils.getColumnName as getCol
import search_count as search
import train_keyword_product
import suggestHomepage as suggest
import pandas as pd
import random

#df = sc.insert_data("banana",3)
#list = [1,2,3,4,6]
#sc.insert_data_related(15417, list)
#sc.find_title(1)
#for i in range (1, 25641):
#    search.subtitle(i)
#for i in range (1084, 25642):
#    search.subtitle(i)
#train.train_keyword()
#for i in range (1, 501):
#    sc.cal_interaction_score(i)
mostpo, Xtab, decom = suggest.setmodel()
#print(mostpo)
#print(len(Xtab))
#print(decom)
#may_buy = suggest.suggestmain(200, mostpo, Xtab, decom)
#print(may_buy)
#new_user = suggest.newusersuggestion(mostpo)
#print(mostpo)
#print(len(new_user))
group = suggest.preparing_data()
#print(group[(group['price_category'] ==1)  & (group['category_code']==1)])
#print(group[(group['price_category'] ==5)  & (group['category_code']==1)])
#print("GG")
#print(group.describe(include = 'category'))
#df.loc[df['category_code']==1,'price_category'] = pd.qcut(df.loc[df['category_code'] == 1]['price'],5,labels=[1,2,3,4,5])
#print(df.loc[df['category_code']==2, 'price_category'])
#for i in df['category_code'].unique():
#    df.loc[df['category_code']==i,'price_category'] = pd.qcut(x=df['price'][df['category_code']==i],q=5,labels=[1,2,3,4,5])
#print(group)

#content_df = suggest.model_implementation(group)
#print(content_df)
#products = suggest.predict_homepage(content_df, 2,mostpo)
#print(products)
df = sc.query_most_interaction_product()
df = pd.DataFrame(df, columns=['product_id', 'score'])
products = df['product_id'][:160].sample(frac=1)
print(type(products[:120].values.tolist()))

