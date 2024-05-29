from flask import Flask, request
import requests
import logging

app = Flask(__name__)

# Correct Flowise API URL
FLOWISE_API_URL = "https://raoulbia-cybc.hf.space/api/v1/prediction/d2c3c7dc-dc96-4501-9b5b-6d79db4fcaaf"
TELEGRAM_BOT_TOKEN = ''
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    return "Hello, World!"
    
@app.route('/webhook', methods=['POST'])
def webhook():
    app.logger.debug("Received a request to /webhook")
    data = request.get_json()
    app.logger.debug(f"Request data: {data}")
    if data and 'message' in data and 'chat' in data['message'] and 'id' in data['message']['chat'] and 'text' in data['message']:
        chat_id = data['message']['chat']['id']
        message = data['message']['text']
        
        app.logger.debug(f"Received message: {message} from chat_id: {chat_id}")

        try:
            response = get_flowise_response(message)
            app.logger.debug(f"Flowise response: {response}")
            send_message(chat_id, response)
        except Exception as e:
            app.logger.error(f"Error handling the message: {e}")
            send_message(chat_id, "Sorry, something went wrong.")
        return "ok"
    else:
        app.logger.error("Invalid request data")
        return "invalid request", 400

def get_flowise_response(message):
    payload = {
        "question": message
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(FLOWISE_API_URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        app.logger.debug(f"Flowise API raw response: {response.text}")
        return response.json().get('text', 'Sorry, I could not get an answer.')
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error communicating with Flowise API: {e}")
        return "Sorry, something went wrong with the Flowise API."
    except ValueError as e:
        app.logger.error(f"Error parsing JSON response from Flowise API: {e}")
        return "Sorry, something went wrong with the Flowise API."


def send_message(chat_id, text):
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    try:
        response = requests.post(TELEGRAM_API_URL, json=payload, timeout=10)
        response.raise_for_status()
        app.logger.debug(f"Telegram API response: {response.json()}")
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error sending message to Telegram API: {e}")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
