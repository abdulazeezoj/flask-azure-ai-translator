from flask import Flask, request, render_template
import os
import uuid
from dotenv import load_dotenv
import requests


# Load environment variables
load_dotenv()

# Create a Flask application
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/translate', methods=['POST'])
def translate():
    # Get request data
    data = request.get_json()
    # Get the text to translate
    src_text = data['src-text']
    # Get the language to translate to
    trans_lang = data['trans-lang']

    # Load the API key from the environment variables
    key = os.getenv('KEY')
    endpoint = os.getenv('ENDPOINT')
    location = os.getenv('LOCATION')

    # Prepare API path and parameters
    path = '/translate?api-version=3.0'
    params = f'&to={trans_lang}'

    # Create full API url
    api_url = endpoint + path + params

    # Create request headers
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-Type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # Create request body
    body = [{'text': src_text}]

    # Make the request (using POST)
    translator_request = requests.post(api_url, headers=headers, json=body)
    # Retrieve the response
    translator_response = translator_request.json()

    # Extract the source language and the translated text
    src_lang = translator_response[0]['detectedLanguage']['language']
    trans_text = translator_response[0]['translations'][0]['text']
    chk_lang = translator_response[0]['translations'][0]['to']

    # Return the translated text
    if chk_lang == trans_lang:
        result = {
            'status': 'ok',
            'src_text': src_text,
            'src_lang': src_lang,
            'trans_text': trans_text
        }
    else:
        result = {
            'status': 'bad'
        }

    return result
