from flask import Flask, request, jsonify
from pytrends.request import TrendReq

app = Flask(__name__)

@app.route('/trend', methods=['POST'])
def get_trends():
    try:
        data = request.get_json()
        keywords = data.get('keywords', [])

        if not keywords:
            return jsonify({'error': 'キーワードがありません'}), 400

        pytrends = TrendReq(hl='ja-JP', tz=540)
        pytrends.build_payload(keywords, timeframe='now 7-d', geo='JP')
        trend_data = pytrends.interest_over_time()

        result = {}
        for kw in keywords:
            if kw in trend_data.columns:
                score = trend_data[kw].mean()
                result[kw] = int(score)
            else:
                result[kw] = 0

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
