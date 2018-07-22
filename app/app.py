import requests
import json
from flask import Flask, request

from . import chatbot

# FB messenger credentials
ACCESS_TOKEN = "EAAGwOQvq9J4BAL8iDnEVUpkfZBuY2pgkuLjD8aXxkF4LZAz8pEPtir96ZBJIHXiq3ZCUfLMd8ZAjbVQEmZCCkPJAeCL0GW9yT24W6E797pz4LTK68luVTSNiBXFbkZBh3v93rOKkHFqKReStnAZBOOAmzoOB6l5SmDJ47X6yHgL8tgZDZD"

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # our endpoint echos back the 'hub.challenge' value specified when we setup the webhook
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == '123stella#':
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return 'Hello World (from Flask!)', 200

def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)


@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    message = data['entry'][0]['messaging'][0]['message']['text']
    response = chatbot.response(message)

    if response:
        reply(sender, response)

    return "ok"

if __name__ == '__main__':
    app.run(debug=True)