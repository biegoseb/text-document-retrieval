from flask import Flask, request, Response
from flask_cors import CORS
from inverted_index import InvertedIndex
import json, sys

app = Flask(__name__)
inverted_index = InvertedIndex()

CORS(app)

@app.route('/query/<index>', methods=["POST"])
def query(index):
    req = request.get_json()
    doc = inverted_index.compare_query(req['query'])
    #print(doc[int(index)])
    f = open(doc[int(index)]['docId'], encoding='utf-8')
    file = json.loads(f.read())
    tweets_ids = []
    for x in range(len(doc[int(index)]["results"])):
        tweets_ids.append((doc[int(index)]["results"][x]["tweets"]))
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
    inverted_index.create_inverted_index()
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))
