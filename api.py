import random
from flask import Flask, request
from pymessenger.bot import Bot
import crypto
from dotenv import dotenv_values
config = dotenv_values(".env")

app = Flask(__name__)
ACCESS_TOKEN = config['ACCESS_TOKEN']
VERIFY_TOKEN = config['VERIFY_TOKEN']
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
                        user_message = message['message'].get('text').lower()
                        #function that takes name of crypto and return a few informations
                        print(user_message)
                        response = crypto.get_info(user_message)
                        send_message(recipient, response)
                    if message['message'].get('attachments'):
                        response = "Sorry I don't handle this type of files at the moment :/"
                        send_message(recipient, response)
    return "Message Processed!"

# Function that sends every x period value of specific crypto
def verify_token(token):
    if token == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid Verification Token'



def send_message(recipient_id, response):
    # Sends User the text message provided via input response parameter
    bot.send_image_url(recipient_id, "https://media.giphy.com/media/Ogak8XuKHLs6PYcqlp/giphy.gif")
    bot.send_text_message(recipient_id, response)
    return "Success"

if __name__ == '__main__':
    app.run()
    
    
#TODO: Send updates automatically for a specific cryptocurrency or more than one
#TODO: Subscription Flow -> Yo activates the flow to make you subscribe
#TODO: No database just a JSON File with (Recipient_ID: ['DOGE', 'XRP'])