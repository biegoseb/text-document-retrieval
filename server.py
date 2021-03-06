from flask import Flask, request, Response
from flask_cors import CORS
from inverted_index import InvertedIndex
import json, sys

app = Flask(__name__)
index = InvertedIndex()

CORS(app)

@app.route('/query/<id>', methods=["POST"])
def query(id):
    req = request.get_json()
    doc = index.compare_query(req['query'])
    #print(doc[int(id)])
    f = open(doc[int(id)]['docId'], encoding='utf-8')
    file = json.loads(f.read())
    tweets_ids = []
    for x in range(len(doc[int(id)]["results"])):
        tweets_ids.append((doc[int(id)]["results"][x]["tweets"]))
    print(tweets_ids)
    tweets = []
    for x in tweets_ids:
        for tweet in x:
            for j in file:
                if tweet['tweet_id'] == j['id']:
                    j['id'] = str(j['id'])
                    j['user_id'] = str(j['user_id'])
                    tweets.append(j)
    f.close()
    return Response(json.dumps(tweets), status = 202, mimetype="application/json")

if __name__ == '__main__':
    index.create_inverted_index()
    #sys.stdout = open('inverted_index.txt', 'w')
    #sys.stdout.reconfigure(encoding = 'utf-8')
    #data_to_print = sorted(index.inverted_index.items())
    #for token in data_to_print:
    #  data = json.dumps(token)
    #  print(data)
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))
