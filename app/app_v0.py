from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import requests
import logging

app = Flask(__name__)

# Flowise API URL
API_URL = "https://raoulbia-cybc.hf.space/chatbot/d2c3c7dc-dc96-4501-9b5b-6d79db4fcaaf"

# Function to query Flowise
def query(payload):
    response = requests.post(API_URL, json=payload)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    return "Hello, World!"
    

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').strip()
    app.logger.debug(f"Received message: {incoming_msg}")
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    if incoming_msg:
        try:
            # Query Flowise API
            flowise_response = query({"question": incoming_msg})
            app.logger.debug(f"Flowise response: {flowise_response}")
            if 'text' in flowise_response:
                msg.body(flowise_response['text'])
                responded = True
            else:
                msg.body('No response found in Flowise response.')
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Request to Flowise failed: {e}")
            msg.body('Flowise service is unavailable.')

    if not responded:
        msg.body('Sorry, I could not understand your message.')

    return str(resp)

@app.route("/status_callback", methods=['POST'])
def status_callback():
    status = request.values.get('MessageStatus', '')
    message_sid = request.values.get('MessageSid', '')
    app.logger.debug(f"Message SID: {message_sid}, Status: {status}")
    # Handle the status update as needed (e.g., logging, updating a database, etc.)
    return '', 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
