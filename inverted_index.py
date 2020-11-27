import unicodedata
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import re, string
import os
import sys
from os.path import isfile, join
import json
import math
import numpy as np

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

  def create_doc(self, file, id):
    doc = {
            "doc_id": file,
            "tweets": [
                        {
                          "tweet_id": id,
                          "freq": 1
                        }
                      ]
          }
    return doc

  def create_inverted_index(self):
    self.read_files()
    for file in self.tweets_files:
      json_file = open(file, encoding = 'utf-8').read()
      text_list = [(e['text'],e['id']) for e in json.loads(json_file) if not e["retweeted"]]
      for text in text_list:
        t = text[0]
        t = self.clean_text(t.lower())
        for word in t:
          if word not in stoplist:
            token = stemmer.stem(word)
            if token not in self.inverted_index.keys():
              self.inverted_index[token] = { }
            if file not in self.inverted_index[token].keys():
              self.inverted_index[token][file] = {"tf":0}
              self.inverted_index[token][file]["tweets"] = [ ]
            found = False
            for x in self.inverted_index[token][file]["tweets"]:
              if x["tweet_id"] == text[1]:
                found = True
                x["freq"] += 1
                break
            if not found:
              self.inverted_index[token][file]["tweets"].append({"tweet_id":text[1], "freq":1})
            self.inverted_index[token][file]["tf"] += 1
      print(file)
    for token in self.inverted_index:
      token["idf"] = math.log(len(self.tweets_files)/len(token[]), 10)

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

'''
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
'''