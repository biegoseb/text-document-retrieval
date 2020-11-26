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

nltk.download('stopwords')
nltk.download('punkt')

ROOT = "./"
EXT = ".json"
BEG = "tweets_2018-"

#abc = []
#for c in string.ascii_lowercase[:27]:
#	abc.append(c)
#abc.append('ñ')
#abc.append('á')
#abc.append('é')
#abc.append('í')
#abc.append('ó')
#abc.append('ú')
#abc.append('')
#print(abc)

def remove_espacial_character(txt):
	characters = ('\"','\'','º','&','¿','?','¡','!',' “','…','👏',
								'-','—','‘','•','›','‼','€','£','↑','→','↓','↔',
								'↘','↪','√','∧','⊃','⌒','⌛','⏬','⏯','⏰','⏹')
	for character in characters:
		txt = txt.replace(character, "")
	return txt

def remove_punctuation ( text ):
  return re.sub('[%s]' % re.escape(string.punctuation), ' ', text)

def remove_emoji(txt):
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
  return re.sub(emoj, '', txt)

def recovery(list):
	print(list)

def AND(list1,list2):
	list_res=[]
	min_=min(len(list1),len(list2))
	j=0
	k=0
	for i in range(min_):
		if(list1[j]==list2[k]):
			list_res.append(list1[j])
			j+=1
			k+=1
		elif(int(list1[j][-5])<int(list2[k][-5])):
			j+=1
		else:
			k+=1
	return list_res

def OR(list1,list2):
	list_rest=[]
	j=0
	k=0
	while(j<len(list1) and k<len(list2)):
		if(list1[j]==list2[k]):
			list_rest.append(list1[j])
			j+=1
			k+=1
		elif(int(list1[j][-5])<int(list2[k][-5])):
			list_rest.append(list1[j])
			j+=1
		else:
			list_rest.append(list2[k])
			k+=1
	if(j!=k):
		if(j==len(list1)):
			list_rest+=list2[k:len(list2)]
		else:
			list_rest+=list1[j:len(list1)]
	return list_rest

def AND_NOT(list1,list2):
	list_res=[]
	j=0
	k=0
	while(j<len(list1) and k<len(list2)):
		if(list1[j]==list2[k]):
			j+=1
			k+=1
		elif(int(list1[j][-5])<int(list2[k][-5])):
			list_res.append(list1[j])
			j+=1
		elif(int(list1[j][-5])>int(list2[k][-5])):
			k+=1
	if(j<len(list1)):
		list_res+=list1[j:len(list1)]
	return list_res

def L(key):
	_token=stemmer.stem(key.lower())
	return data[_token]

class Document:
	tweet = ""
	count = 0
	tweets_ids = []
	def __init__(self, tweet, count):
		self.tweet = tweet
		self.count = count

# {word : tweet}
index = {}
tweets = []
for base, dirs, files in os.walk(ROOT):
    for file in files:
        f = join(base, file)
        if f.endswith(EXT) and BEG in f:
            tweets.append(f)

stoplist = stopwords.words("spanish")
stoplist += ['?','aqui','.',',','»','«','â','ã','>','<','(',')','º','u']
stemmer = SnowballStemmer('spanish')

c=1
for tweet in tweets:
	json_tweet = open(tweet, encoding = 'utf-8').read()
	text_list = [(e['text'],e['id']) for e in json.loads(json_tweet) if not e["retweeted"]]
	tokens = []
	for txt in text_list:
		txt = txt[0]
		t = txt.find('https://t.co/')
		if t != -1:
			txt = re.sub('https://t.co/\w{10}', '', txt)
		txt = remove_espacial_character(remove_punctuation(txt.lower()))
		txt = remove_emoji(txt)
		txt = nltk.word_tokenize(txt)
		for word in txt:
			if word not in stoplist:
				_token = stemmer.stem(word)
				if not _token in index:
					index[_token] = {}
					index[_token]['tweets'] = []
					index[_token]['weight'] = 1
				else:
					index[_token]['weight'] += 1
				if len(index[_token]['tweets']) > 0:
					if tweet != index[_token]['tweets'][-1].tweet:
						doc = Document(tweet, 1)
						index[_token]['tweets'].append(doc)
					else:
						index[_token]['tweets'][-1].count += 1
				else:
					doc = Document(tweet, 1)
					index[_token]['tweets'].append(doc)
	print(f"{c}")
	c+=1
		

sorted_data = sorted(index, key = lambda v: len(index[v]['tweets']), reverse = True)

data = {}
for i in sorted_data:
	if not i in data:
		data[i] = []
	data[i] = index[i]['tweets']

print("carajo")
sys.stdout = open('inverted_index.txt', 'w')
sys.stdout.reconfigure(encoding = 'utf-8')
data_to_print = sorted(data.items())


for key, value in data_to_print:
	print(key, f"(w:{index[key]['weight']}", end="")
	tf = 0
	idf = math.log(len(tweets)/len(value), 10)	
	for v in value:
		tf += 1 + math.log(v.count, 10)
		print("[", v.tweet, ",", v.count, "]", end=",")
	print(f"(tf:{round(tf, 2)})", end=",")
	print(f"(idf:{round(idf, 2)})", end=",")
	print(f"(TF-IDF:{round(tf*idf, 2)})")

def cosine(q, doc):
  return np.dot(q, doc) / (np.linalg.norm(q) * np.linalg.norm(doc))

def get_terms(query_text):
	query_text = remove_espacial_character(remove_punctuation(query_text.lower()))
	query_text = remove_emoji(query_text)
	query_text = nltk.word_tokenize(query_text)
	tokens = []
	for word in query_text:
			if word not in tokens:
				tokens.append(word)
	tokens_clean = tokens.copy()
	for token in tokens:
		if token in stoplist:
			tokens_clean.remove(token)
	stemmed_tokens = []
	for token in tokens_clean:
		token = stemmer.stem(token)
		stemmed_tokens.append(token)
	return stemmed_tokens

def get_TFIDF(query_terms):	
	tf_idf_list = []
	for t in query_terms:
		tf = 0
		idf = math.log(len(tweets)/len(data[t]), 10)
		for doc in data[t]:
			tf += 1 + math.log(doc.count, 10)
		tf_idf_list.append(round(tf*idf,2))
	return tf_idf_list

def get_document(i, query_terms):
	pass

def retrievalCosine1(collection, query_text): #query : texto
  result = []
  query_terms = get_terms(query_text)
  query = get_TFIDF(queryTerms) #tf-idf del query        
  for i in range(len(collection)):        
      doc = collection.get_document(i, query_terms); #tf-idf del documento
      sim = cosine(query, doc)
      result.append( (doc.id, sim) )#[ (doc1, sc1), (doc, sc2) ]    
  result.sort(key = lambda  tup: tup[1])
  return result

#q = input("Ingrese consulta: ")
#t = get_terms(q)

for doc in data["aventaj"]:
	print(doc.tweet)

#sys.stdout = open('index2.txt', 'w')
#sys.stdout.reconfigure(encoding = 'utf-8')