from flask import Flask, request, jsonify, render_template
import os
from stocks import get_price, parse_date, str2date, get_recommendation

app = Flask(__name__)


@app.route('/')
def index():
    return 'Webhook up and running!'


@app.route('/stocks', methods=['POST'])
def get_info():
    data = request.get_json(silent=True)
    print(data)

    intent = data['queryResult']['intent']['displayName']

    if intent == 'Price Intent':
        try:
            date = data['queryResult']['parameters']['date-time']
            price = get_price(parse_date(date))
            response = 'The price in ' + str2date(parse_date(date)) + ' is ' + str(price) + '$'
        except:
            response = 'The date you are trying to request is not available.'
    
    elif intent == 'Recommendation Intent':
        response = get_recommendation()
    
    else:
        response = 'I dunno.'
    
    reply = {
        "fulfillmentText": response,
    }

    return jsonify(reply)


# run Flask app
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT'))
