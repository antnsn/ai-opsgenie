from flask import Flask, request, jsonify, abort
import openai
import os
import requests
import logging
import functools
import json 

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

opsgenie_url = os.getenv('OPSGENIE_URL', 'https://api.opsgenie.com/v2/alerts')


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
        structured_data = get_structured_data(data)
        # Optionally send structured data to Opsgenie or handle it as needed
        # response = send_to_opsgenie(data, structured_data)
        # For now, let's just return the structured data for inspection
        return jsonify({"status": "success", "data": structured_data}), 200
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

def get_structured_data(data):
    try:
        description = data['message']
        prompt_text = f"""
        Based on the following description, fill out the structured data:

        Description: {description}

        Fill in the following fields:
        Source:
        Tags: []
        Details: {{}}
        Entity:
        Priority:

        Please format your response as a JSON object.
        """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Please generate structured data based on the description."},
                      {"role": "user", "content": prompt_text}],
        )
        structured_response = response['choices'][0]['message']['content'].strip()
        
        return json.loads(structured_response)

    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON from OpenAI: {str(e)}")
        raise ValueError("Received malformed JSON from OpenAI.")

    except Exception as e:
        logging.error(f"Failed to generate structured data from OpenAI: {str(e)}")
        raise


def send_to_opsgenie(data):
    headers = {
        "Authorization": f"GenieKey {opsgenie_api_key}",
        "Content-Type": "application/json"
    }
    # Assuming 'data' is already a structured dictionary fitting Opsgenie's API
    try:
        response = requests.post(opsgenie_url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Failed to send structured data to Opsgenie: {str(e)}")
        raise


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
