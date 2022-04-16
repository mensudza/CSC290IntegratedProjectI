import search_count as sc

def train_keyword() :
    df = sc.read_df()
    df_clean = sc.full_cleaning(df)
    sc.learn_relation_keyword(df_clean)

if __name__ == '__main__':
    train_keyword()