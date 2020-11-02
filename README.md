# Webhook

Heroku deploy of a web hook to attend Dialogflow requests

## Enviroment Variables

You will need the Dialogflow Project ID and the Agent.json file.

.env file:
'''
DIALOGFLOW_PROJECT_ID=<Your project ID>
GOOGLE_APPLICATION_CREDENTIALS=<File Path>
LC_ALL=C.UTF-8
LANG=C.UTF-8
'''

## Development

- **Ngrok**. Just download from the website.

- **Api**. I used an API I developed for bollinger bands info

## Production

Heroku