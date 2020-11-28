import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import re, string
import os
import sys
from os.path import join
import json
import math

ROOT = "./"
EXT = ".json"
BEG = "tweets_2018-"

nltk.download('stopwords')
nltk.download('punkt')
stoplist = stopwords.words("spanish")
stoplist += ['?','aqui','.',',','»','«','â','ã','>','<','(',')','º','u']
stemmer = SnowballStemmer('spanish')

class InvertedIndex:
  inverted_index = { }
  tweets_files = [ ]
  tweets_count = 0

  def read_files(self):
    for base, dirs, files in os.walk(ROOT):
      for file in files:
        f = join(base, file)
        if f.endswith(EXT) and BEG in f:
          self.tweets_files.append(f)
  
  def remove_punctuation(self, text):
    return re.sub('[%s]' % re.escape(string.punctuation), ' ', text)

  def remove_emoji(self, text):
    emoj = re.compile("["
      u"\U0001F600-\U0001F64F"  # emoticons
      u"\U0001F300-\U0001F5FF"  # symbols & pictographs
      u"\U0001F680-\U0001F6FF"  # transport & map symbols
      u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
      u"\U00002500-\U00002BEF"  # chinese char
      u"\U00002702-\U000027B0"
      u"\U00002702-\U000027B0"
      u"\U000024C2-\U0001F251"
      u"\U0001f926-\U0001f937"
      u"\U00010000-\U0010ffff"
      u"\u2640-\u2642" 
      u"\u2600-\u2B55"
      u"\u200d"
      u"\u23cf"
      u"\u23e9"
      u"\u231a"
      u"\ufe0f"  # dingbats
      u"\u3030"
                    "]+", re.UNICODE)
    return re.sub(emoj, '', text)

  def remove_url(self, text):
    t = text.find('https://t.co/')
    if t != -1:
      text = re.sub('https://t.co/\w{10}', '', text)
    return text

  def remove_special_character(self, text):
    characters = ('\"','\'','º','&','¿','?','¡','!',' “','…','👏',
								'-','—','‘','•','›','‼','€','£','↑','→','↓','↔',
								'↘','↪','√','∧','⊃','⌒','⌛','⏬','⏯','⏰','⏹')
    for char in characters:
      text = text.replace(char, "")
    return text

  def clean_text(self, text):
    text = self.remove_special_character(text)
    text = self.remove_punctuation(text)
    text = self.remove_emoji(text)
    text = self.remove_url(text)
    text = nltk.word_tokenize(text)
    return text

  def create_inverted_index(self):
    self.read_files()
    cont = 0
    for file in self.tweets_files:
      #file = self.tweets_files[0]
      json_file = open(file, encoding = 'utf-8')
      text_list = [(e['text'],e['id']) for e in json.loads(json_file.read()) if not e["retweeted"]]
      json_file.close()
      for text in text_list:
        self.tweets_count += 1
        t = text[0]
        t = self.clean_text(t.lower())
        for word in t:
          if word not in stoplist:
            token = stemmer.stem(word)
            if token not in self.inverted_index.keys():
              self.inverted_index[token] = {"df":0, "tweets":[ ]}
            if len(self.inverted_index[token]["tweets"]) > 0:
              if self.inverted_index[token]["tweets"][-1]["id"] != text[1]:
                self.inverted_index[token]["df"] += 1
                self.inverted_index[token]["tweets"].append({"id":text[1], "tf":1,"doc":file})
              else:
                self.inverted_index[token]["tweets"][-1]["tf"] += 1
            else:
              self.inverted_index[token]["df"] += 1
              self.inverted_index[token]["tweets"].append({"id":text[1], "tf":1,"doc":file})        
      cont += 1
      print(cont, file)
    self.calculate_tf_idf()
    self.normalize()

  def calculate_tf_idf(self):
    for token in self.inverted_index.keys():
      self.inverted_index[token]["idf"] = math.log10(self.tweets_count/self.inverted_index[token]["df"])
      self.inverted_index[token]["score"] = 0
      idf = self.inverted_index[token]["idf"]
      for tweet in self.inverted_index[token]["tweets"]:
        tf = tweet["tf"]     
        tf_idf = (1 + math.log10(tf)) * idf
        tweet["tf_idf"] = tf_idf
        self.inverted_index[token]["score"] += tf_idf
  
  def normalize(self):
    doc = self.tweets_files[0]
    json_file = open(doc, encoding = 'utf-8')
    for tweet in json.loads(json_file.read()):
      if not tweet["retweeted"]:
        norma = 0
        txt = self.clean_text(tweet["text"].lower())
        for word in txt:
          if word not in stoplist:
            word = stemmer.stem(word)
            t = [x for x in self.inverted_index[word]["tweets"] if x["id"] == tweet["id"]]
            norma += t[0]["tf_idf"]**2
        norma = math.sqrt(norma)
        for word in txt:
          if word not in stoplist:
            word = stemmer.stem(word)
            t = [x for x in self.inverted_index[word]["tweets"] if x["id"] == tweet["id"]]
            t[0]["norma"] = t[0]["tf_idf"]/norma
    json_file.close()

  def compare_query(self, query):
    query = self.clean_text(query.lower())
    index_query = {}
    for word in query:
      if word not in stoplist:
        word = stemmer.stem(word)
        if word not in index_query.keys():
          index_query[word] = { "tf" : 0 }
        index_query[word]["tf"] += 1
    norma = 0
    for word in index_query.keys():
      if word in self.inverted_index.keys():
        index_query[word]["tf_idf"] = (1+math.log10(index_query[word]["tf"])) * self. inverted_index[word]["idf"]
        norma += index_query[word]["tf_idf"]**2
    norma = math.sqrt(norma)
    for word in index_query.keys():
      if "tf_idf" in index_query[word].keys():
        index_query[word]["norma"] = index_query[word]["tf_idf"]/norma if norma != 0 else 0
    cosenos = []
    for file in self.tweets_files:
      json_file = open(file, encoding = 'utf-8')
      for tweet in json.loads(json_file.read()):
        if not tweet["retweeted"]:
          similarity = 0
          for word in index_query.keys():
            t = [x for x in self.inverted_index[word]["tweets"] if x["id"] == tweet["id"]]
            if "norma" in index_query[word].keys() and len(t) > 0:
              print(t)
              similarity += index_query[word]["norma"] * t[0]["norma"]
          cosenos.append({"id":tweet["id"], "doc":file, "cosin":similarity})
    cosenos = sorted(cosenos, key = lambda v: v["cosin"], reverse=True)
    return cosenos
    

'''
def main():
  index = InvertedIndex()
  index.create_inverted_index()
  sys.stdout = open('inverted_index.txt', 'w')
  sys.stdout.reconfigure(encoding = 'utf-8')
  data_to_print = sorted(index.inverted_index.items())
  #for token in data_to_print:
  #  data = json.dumps(token)
  #  print(data)
  for key, value in data_to_print:
    print(key,value)

main()

index = {          
          "carajo": {
            "idf": 0.65, (log(N/len(docs))),
            "score": sum(docs[i].tf_idf),
            "tweets_2018-08-07": {
                    "tf": 58, sum(tweets[i].freq)
                    "tf_idf":  (1 + log(tf)) * idf,
                    "norma": tf_idf/norm
                    "tweets": [
                                {
                                  "tweet_id": 12345,
                                  "freq": 10
                                },
                                {},{},...
                              ]
                  }
          },
          "reggiar": {},
          {}, ...   
        }

El señor Daniel Urresti me bloqueo por cuestionar continuamente su candidatura
['senor', 'daniel', 'urresti', 'bloqueo', 'cuestionar', 'continuamente', 'candidatura']
['sen', 'daniel', 'urresti', 'bloque', 'cuesti', 'continu', 'cand']
[ {
    'sen': {
      'tf': frecuencia de la palabra en el query
      'tf-idf': tf*idf
      'norma': tf-idf/norm
    }, 
    'daniel': {
      'tf': frecuencia de la palabra en el query
      'tf-idf': tf*idf
      'norma': tf-idf/norm
    },
    'urresti': {
      'tf': frecuencia de la palabra en el query
      'tf-idf': tf*idf
      'norma': tf-idf/norm
    },
    'bloque': {
      'tf': frecuencia de la palabra en el query
      'tf-idf': tf*idf
      'norma': tf-idf/norm
    }, 
    'cuesti': {
      'tf': frecuencia de la palabra en el query
      'tf-idf': tf*idf
      'norma': tf-idf/norm
    }, 
    'continu': {
      'tf': frecuencia de la palabra en el query
      'tf-idf': tf*idf
      'norma': tf-idf/norm
    }, 
    'cand' : {
      'tf': frecuencia de la palabra en el query
      'tf-idf': tf*idf
      'norma': tf-idf/norm
    }
  }]

index = {          
          "carajo": {
            "df": nº de tweets en los que aparece la palabra del total (20 mil)
            "idf": math.log10(20000/len(tweets)),
            "score": sum(tweets[i].tf_idf),
            "tweets": [
              {
                "id": 1234134134
                "tf": nº de veces que se repite la palabra en el tuit
                "tf_idf": (1 + log(tf)) * idf,
                "norma": tf_idf/norm
              }
            ]
          },
          "reggiar": {
            "df": nº de tweets en los que aparece la palabra del total (20 mil)
            "idf": math.log10(20000/len(tweets)),
            "score": sum(tweets[i].tf_idf),
            "tweets": [
              {
                "id": 1234134134
                "tf": nº de veces que se repite la palabra en el tuit
                "tf_idf": (1 + log(tf)) * idf,
                "norma": tf_idf/norm
              }
            ]
          },  
        }
'''