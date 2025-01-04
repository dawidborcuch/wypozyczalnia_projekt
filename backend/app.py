from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/main-site')
def main_site():
    url = 'https://dobrapogoda24.pl/api/v1/weather/simple?city=warszawa&day=1&token=d21cbfc6141eaa3c1b71'
    response = requests.get(url)
    data = response.json()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
