from flask import Flask, render_template, request
import requests
import os


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route('/api/<coin>')
def get_coin_data(coin): 
    base_url = 'https://rest.coinapi.io/v1/exchangerate/'
    COIN_API_KEY = os.getenv('COIN_API_KEY')
    headers = {'X-CoinAPI-Key': COIN_API_KEY}
    rest_of_query = '/USD/history?period_id=1MIN&time_start=2022-01-01T00:00:00&time_end=2022-05-10T00:00:00'
    request_url = base_url + coin + rest_of_query
    response = requests.get(request_url, headers=headers)
    data = response.json()
    return f'<p>{data}</p>'

# @app.route("/api/<coin>")
# def get_coin_data(coin): 
#     base_url = 'https://rest.coinapi.io/v1/exchangerate/'
#     headers = 
# COIN_API_KEY=
# # url = 'https://rest.coinapi.io/v1/exchangerate/BTC/USD'
# url = 'https://rest.coinapi.io/v1/exchangerate/BTC/USD/history?period_id=1MIN&time_start=2022-01-01T00:00:00&time_end=2022-05-10T00:00:00'
# headers = {'X-CoinAPI-Key': }
# response = requests.get(url, headers=headers)
# data = response.json()