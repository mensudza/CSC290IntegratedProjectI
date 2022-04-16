import search_count as search
import connectDB as conn
import pandas as pd
#print(search.keyword("Hi I am Spain"))
'''df = pd.DataFrame([[1,"HOUZE - 6 Tier 'Apple' Knock Down Cabinet"],
                   [2,'AVALON Apple Cider Vinegar Gummies 60s'],
                   [3,"HOUZE - 6 Tier 'Apple' Knock Down Cabinet"],
                   [4,"21st Century Apple Cider Vinegar 90 Gummies"],
                   [5,"SKINARMA Tekubi Apple Watch Strap 42/44mm"]], columns = ['id','title'])

df = search.read_csv('./csv/cshop_ml_public_product.csv')
#df_clean = search.full_cleaning(df)
#search.learn_relation_keyword(df_clean)
ai_index = search.learn_relation_title(df, './model/keyword2vec_model.bin')
products = search.search_and_show(ai_index, 'apple')'''
print(conn.get_search_dataframe())