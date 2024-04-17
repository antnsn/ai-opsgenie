from flask import Flask, request, jsonify
import openai
import os
import requests

app = Flask(__name__)

openai_api_key = os.getenv('OPENAI_API_KEY')
openai_url= os.getenv('OPENAI_URL')
opsgenie_api_key = os.getenv('OPSGENIE_API_KEY')
opsgenie_url = os.getenv('OPSGENIE_URL')

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.json
    explanation = get_explanation(data)
    send_to_opsgenie(data, explanation)
    return jsonify({"status": "success"}), 200

def get_explanation(data):
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Explain this message: {data['message']}",
        max_tokens=60,
        api_key=openai_api_key
    )
    return response.choices[0].text.strip()

def send_to_opsgenie(data, explanation):
    url = opsgenie_url
    headers = {
        "Authorization": f"GenieKey {opsgenie_api_key}",
        "Content-Type": "application/json"
    }
    body = {
        "message": data['message'],
        "description": explanation,
        "priority": "P1"  # example priority
    }
    response = requests.post(url, json=body, headers=headers)
    return response.json()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
