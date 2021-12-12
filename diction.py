import requests
from flask import Flask

app = Flask(__name__)


@app.route('/<word>')
def get_info(word):

    url = 'https://api.dictionaryapi.dev/api/v2/entries/en/{}'.format(word)

    response = requests.get(url)

# return a custom response if an invalid word is provided
    if response.status_code == 404:
        error_response = 'We are not able to provide any information about your word. Please confirm that the word is ' \
                         'correctly spelt or try the search again at later time.'
        return error_response

    data = response.json()[0]

    return data




