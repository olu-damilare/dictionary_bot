import os
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
                         'correctly spelt or try the search again at a later time.'
        return error_response

    data = response.json()[0]

    print(data)
    return data


get_info("food")


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
