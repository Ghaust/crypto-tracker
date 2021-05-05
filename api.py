import random
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = 'ACCESS_TOKEN'
VERIFY_TOKEN = 'VERIFY_TOKEN'
bot = Bot(ACCESS_TOKEN)

@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        token = request.args.get("hub.verify_token")
        return verify_token(token)
    else:
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    recipient = message['sender']['id']
                    if message['message'].get('text'):
                        response = get_message()
                        send_message(recipient, response)
                    if message['message'].get('attachments'):
                        response = get_message()
                        send_message(recipient, response)
                        
    return "Message Processed!"

def verify_token(token):
    if token == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid Verification Token'

def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)

def send_message(recipient_id, response):
    # Sends User the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "Success"

if __name__ == '__main__':
    app.run()