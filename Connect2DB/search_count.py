#ตัดคำ
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import scriptDB as db
import nltk
#nltk.download('all')

def keyword(text) :
  stop_words = set(stopwords.words('english')).union(set(string.punctuation))
  word_tokens = word_tokenize(text)
  filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
  lemmatizer = WordNetLemmatizer()
  lemmatize_words = [lemmatizer.lemmatize(word) for word in filtered_sentence]
  final_lower_text = [word.lower() for word in lemmatize_words]

  count_keyword = {}
  for keyword in final_lower_text:
    try:
      count_keyword[keyword] += 1
    except KeyError:
      count_keyword[keyword] = 1

  for key in count_keyword.keys():
    db.insert_data(key, count_keyword[key])
  return count_keyword

#Search
# Search engine

import re  # For preprocessing
import pandas as pd  # For data handling
from time import time  # To time our operations
from collections import defaultdict  # For word frequency
import multiprocessing

import spacy  # For preprocessing

import multiprocessing
from coordle.backend.coordle_backend import QueryAppenderIndex
from gensim.models import Word2Vec
from coordle.backend import QueryAppenderIndex

import logging  # Setting up the loggings to monitor gensim
logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt='%H:%M:%S', level=logging.INFO)


def read_csv(csvsource):
  df = pd.read_csv(csvsource)
  return df

def read_df():
  df = db.for_train_search_model()
  return df


def full_cleaning(df):
  nlp = spacy.load("en_core_web_sm", disable=['ner', 'parser'])
  brief_cleaning = (re.sub("[^A-Za-z']+", ' ', str(row)).lower() for row in df['title'])
  t = time()
  txt = [sub_cleaning(doc) for doc in nlp.pipe(brief_cleaning, batch_size=5000, n_threads=-1)]
  print('Time to clean up everything: {} mins'.format(round((time() - t) / 60, 2)))
  df_clean = pd.DataFrame({'clean': txt})
  print('Finish cleaning')
  return df_clean


def sub_cleaning(doc):
  # Lemmatizes and removes stopwords
  # doc needs to be a spacy Doc object
  txt = [token.lemma_ for token in doc if not token.is_stop]
  # Word2Vec uses context words to learn the vector representation of a target word,
  # if a sentence is only one or two words long,
  # the benefit for the training is very small
  if len(txt) > 2:
    return ' '.join(txt)


def learn_relation_keyword(df_clean):
  from gensim.models.phrases import Phrases, Phraser
  sent = [str(row).split() for row in df_clean['clean']]
  phrases = Phrases(sent, min_count=30, progress_per=10000)
  bigram = Phraser(phrases)
  sentences = bigram[sent]
  word_freq = defaultdict(int)
  for sent in sentences:
    for i in sent:
      word_freq[i] += 1
  sorted(word_freq, key=word_freq.get, reverse=True)

  # train
  cores = multiprocessing.cpu_count()
  w2v_model = Word2Vec(min_count=20,
                       window=2,
                       vector_size=300,
                       sample=6e-5,
                       alpha=0.03,
                       min_alpha=0.0007,
                       negative=20,
                       workers=cores - 1)
  t = time()
  w2v_model.build_vocab(sentences, progress_per=10000)
  print('Time to build vocab: {} mins'.format(round((time() - t) / 60, 2)))

  t = time()
  w2v_model.train(sentences, total_examples=w2v_model.corpus_count, epochs=30, report_delay=1)
  w2v_model.save('keyword2vec_model.bin')
  print('Time to train the model: {} mins'.format(round((time() - t) / 60, 2)))

  w2v_model.save('./model/keyword2vec_model.bin')
  print('Finish learning, save model as keyword2vec_model.bin')


def learn_relation_title(df, modelpath='./model/keyword2vec_model.bin'):
  cores = multiprocessing.cpu_count()
  w2v_model = Word2Vec.load(modelpath)
  w2v_model.init_sims(replace=True)
  # To demonstrate how the search engine works, we index on a subset of the documents in the dataframe.
  ai_index = QueryAppenderIndex(w2v_model.wv.most_similar, n_similars=1)

  ai_index.build_from_df(
    df,
    'id',
    'title',
    'title',
    verbose=True,
    use_multiprocessing=True,
    workers=cores - 1
  )
  return ai_index


def search_and_show(ai_index, query, max_results=120, max_body_length=500):
  '''Searches using the AI Index and shows the result

  Args:
      query: Search query
      max_results: Max results to show for each query
  '''

  docs, scores, errmsgs = ai_index.search(query)

  if errmsgs:
    print('The following errors occurred:', errmsgs)
  else:
    related_id_products = []
    if len(docs) == 0:
      return 'Sorry, no results found.'
    else:
      for doc, score in zip(docs[:max_results], scores[:max_results]):
        print(f'{doc.uid}  {str(doc.title)[:70]:<70}  {score:.4f}')
        print('---')
        related_id_products.append(doc.uid)
      return related_id_products

def find_related_product(ai_index, idproduct, max_results=48, max_body_length=500):
  '''Searches using the AI Index and shows the result

    Args:
        query: Search query
        max_results: Max results to show for each query
  '''

  title = db.find_title(idproduct)
  docs, scores, errmsgs = ai_index.search(title)

  if errmsgs:
    print('The following errors occurred:', errmsgs)
  else:
    related_id_products = []
    if len(docs) == 0:
      return 'Sorry, no results found.'
    else:
      for doc, score in zip(docs[:max_results], scores[:max_results]):
        if int(idproduct) != doc.uid:
          print(f'{doc.uid}  {str(doc.title)[:70]:<70}  {score:.4f}')
          print('---')
          related_id_products.append(doc.uid)

      db.insert_data_related(int(idproduct), related_id_products)
      return title, related_id_products

def subtitle(idProduct) :
  text = db.find_title(idProduct)
  stop_words = set(stopwords.words('english')).union(set(string.punctuation))
  word_tokens = word_tokenize(text)
  filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
  lemmatizer = WordNetLemmatizer()
  lemmatize_words = [lemmatizer.lemmatize(word) for word in filtered_sentence]
  final_lower_text = [word.lower() for word in lemmatize_words]
  db.insert_sub_title(idProduct,",".join(i for i in final_lower_text[:5]))
  print("success : " + str(idProduct))

def train_keyword():
  df = read_df()
  df_clean = full_cleaning(df)
  learn_relation_keyword(df_clean)
