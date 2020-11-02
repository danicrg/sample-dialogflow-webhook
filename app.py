from flask import Flask, request, jsonify, render_template
import os
import json

app = Flask(__name__)


@app.route('/')
def index():
    return 'Webhook up and running!'


@app.route('/stocks', methods=['POST'])
def get_info():
    data = request.get_json(silent=True)
    print(data)

    intent = data['queryResult']['intent']['displayName']

    if intent == 'Test Intent':
        day = data['queryResult']['parameters']['date-time']


        response = 'Today is ' + str(day)
    elif intent == 'AnotherSample Intent':
        response = 'OK'
    else:
        response = 'I dunno.'
    
    reply = {
        "fulfillmentText": response,
    }

    return jsonify(reply)


# run Flask app
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT'))
