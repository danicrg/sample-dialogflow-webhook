from flask import Flask, request, jsonify, render_template
import os
import dialogflow
import requests
import json
from elastic import get_elastic_glossary, get_elastic_example

app = Flask(__name__)


@app.route('/')
def index():
    return 'Webhook up and runnin!'


@app.route('/stocks', methods=['POST'])
def get_info():
    data = request.get_json(silent=True)
    print(data)

    intent = data['queryResult']['intent']['displayName']

    if intent == 'Sample Intent':
        response = 'OK'
    elif intent == 'AnotherSample Intent':
        response = 'OK'
    
    reply = {
        "fulfillmentText": response,
    }

    return jsonify(reply)


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)

        return response.query_result.fulfillment_text


@app.route('/send_message', methods=['POST'])
def send_message():
    # socketId = request.form['socketId']
    message = request.form['message']
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    response_text = {"message": fulfillment_text}

    return jsonify(response_text)


# run Flask app
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT'))
