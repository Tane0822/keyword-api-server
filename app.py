from flask import Flask, request, jsonify
from pytrends.request import TrendReq
import time

app = Flask(__name__)

@app.route('/trend', methods=['POST'])
def get_trends():
    keywords = request.json.get('keywords', [])
    pytrends = TrendReq(hl='ja-JP', tz=540)
    result = {}

    for i in range(0, len(keywords), 5):
        chunk = keywords[i:i+5]
        try:
            pytrends.build_payload(chunk, cat=0, timeframe='today 12-m', geo='JP')
            data = pytrends.interest_over_time()
            if not data.empty:
                for kw in chunk:
                    score = int(data[kw].mean()) if kw in data else 0
                    result[kw] = score
            else:
                for kw in chunk:
                    result[kw] = 0
        except:
            for kw in chunk:
                result[kw] = 0
        time.sleep(1)
    return jsonify(result)
