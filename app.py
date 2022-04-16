from flask import Flask, redirect, url_for, request, render_template, session
import os
import uuid
from dotenv import load_dotenv
import requests


# Load environment variables
load_dotenv()

# Create a Flask application
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the data from the form
        original_text = request.form['text']
        target_lang = request.form['language']

        # Translate the text
        translated_text = translate(original_text, target_lang)

    return render_template('index.html',
                           translated_text=translated_text)


def translate(text, target_lang):
    # Load the API key from the environment variables
    key = os.getenv('KEY')
    endpoint = os.getenv('ENDPOINT')
    location = os.getenv('LOCATION')

    # Prepare API path and parameters
    path = '/translate?api-version=3.0'
    params = '&to={}'.format(target_lang)

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
    body = [{'text': text}]

    # Make the request (using POST)
    translator_request = requests.post(api_url, headers=headers, json=body)
    # Retrieve the response
    translator_response = translator_request.json()
    # Extract the translated text
    translated_text = translator_response[0]['translations'][0]['text']

    # Return the translated text
    return translated_text
