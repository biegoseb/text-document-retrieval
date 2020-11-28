from flask import Flask, request, Response
from flask_cors import CORS
from inverted_index import InvertedIndex
import json, sys

app = Flask(__name__)
inverted_index = InvertedIndex()

CORS(app)

@app.route('/query', methods=["POST"])
def query():
    req = request.get_json()
    doc = inverted_index.compare_query(req['query'])
    doc = doc[0:15]
    #print(doc[int(index)])
    tweets = []
    for tweet in doc:
        #print(tweet["cosin"])
        f = open(tweet["doc"], encoding='utf-8')
        file = json.loads(f.read())
        result = [x for x in file if x["id"]==tweet["id"]][0]
        result['id'] = str(result['id'])
        result['user_id'] = str(result['user_id'])
        tweets.append(result)
        f.close()
    return Response(json.dumps(tweets), status = 202, mimetype="application/json")

if __name__ == '__main__':
    inverted_index.create_inverted_index()
    app.secret_key = ".."
    app.run(port=8081, threaded=True, host=('127.0.0.1'))

