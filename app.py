from flask import Flask, request, jsonify, abort
import openai
import os
import requests
import logging
import functools

app = Flask(__name__)

# Setup basic logging
logging.basicConfig(level=logging.INFO)

# Environment variables with basic validation/logging
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    logging.error("OPENAI_API_KEY is not set.")
    exit(1)

opsgenie_api_key = os.getenv('OPSGENIE_API_KEY')
if not opsgenie_api_key:
    logging.error("OPSGENIE_API_KEY is not set.")
    exit(1)

webhook_api_key = os.getenv('WEBHOOK_API_KEY')
if not webhook_api_key:
    logging.error("WEBHOOK_API_KEY is not set.")
    exit(1)

def require_api_key(view_function):
    @functools.wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.headers.get('X-API-Key') and request.headers.get('X-API-Key') == webhook_api_key:
            return view_function(*args, **kwargs)
        else:
            abort(401)  # Unauthorized
    return decorated_function

@app.route('/webhook', methods=['POST'])
@require_api_key
def handle_webhook():
    data = request.json
    if not data or 'message' not in data:
        logging.error("Invalid data received.")
        return jsonify({"status": "error", "message": "Invalid data"}), 400

    try:
        explanation = get_explanation(data)
        response = send_to_opsgenie(data, explanation)
        return jsonify({"status": "success", "opsgenie_response": response}), 200
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

def get_explanation(data):
    try:
        response = openai.Completion.create(
            engine="davinci",
            prompt=f"Explain this message: {data['message']}",
            max_tokens=60,
            api_key=openai_api_key
        )
        return response.choices[0].text.strip()
    except Exception as e:
        logging.error(f"Failed to get explanation from OpenAI: {str(e)}")
        raise

def send_to_opsgenie(data, explanation):
    headers = {
        "Authorization": f"GenieKey {opsgenie_api_key}",
        "Content-Type": "application/json"
    }
    body = {
        "message": data['message'],
        "description": explanation,
        "priority": "P1"  # example priority
    }
    try:
        response = requests.post(opsgenie_url, json=body, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Failed to send data to Opsgenie: {str(e)}")
        raise

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
