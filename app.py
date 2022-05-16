from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
import requests
import os
import pandas as pd
import plotly
import plotly.express as px
import json
import datetime
from datetime import date
# from datetime import date, time, datetime

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/api/<coin>', methods=["GET", "POST"])
def get_coin_data(coin): 
    #Sets the end of our timeframe:
    ending_date = date.today()
    ending_time = "00:00:00"

    #Sets the start of our timeframe to one year prior to present:
    starting_date = ending_date - datetime.timedelta(days=365)

    # print(f"Starting date: {starting_date}\nEnding date: {ending_date}" )

    base_url = 'https://rest.coinapi.io/v1/exchangerate/'
    COIN_API_KEY = os.getenv('COIN_API_KEY')
    headers = {'X-CoinAPI-Key': COIN_API_KEY}
    rest_of_query = f'/USD/history?period_id=1DAY&time_start={starting_date}T{ending_time}&time_end={ending_date}T{ending_time}'
    request_url = base_url + coin + rest_of_query
    response = requests.get(request_url, headers=headers)
    print(response)
    # Data SHOULD be JSON... is it?
    data = response.json()
    # keys = data[0].keys()
    # data = json.dumps(response)
    # new_data = (jsonify({data}))
    # data = response.json()
    df = pd.DataFrame(data)
    print(df)
    # print(f"Number of dictionaries in data: {len(data)}")



    # We just need "time_period_end" and "rate_close" from each of 100 dictionaries
    # X axis is time (time_period_end)
    # Y axis is $$ (rate_close)
    # Each data point is constructed from each dictionary in data

    # PANDAS: Make data frame and chart:
    # df = pd.DataFrame({})
    
    # df = pd.read_json(data)
    # print(df.info)

    # fig = px.line(df, x=keys, y=keys, title="Stonks 📈")
    # graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # if request.method == "POST":
    #     coin_name = request.form.get("coin_name")
    #     return redirect(url_for('app.api', coin=coin_name))

    return f"<p>{df}</p>"
    #return render_template('graph.html', graphJSON = graphJSON)

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


    # data returns an array containing a bunch of dicts like this:
    #{'time_period_start': '2021-05-16T00:00:00.0000000Z', 
    # 'time_period_end': '2021-05-16T00:01:00.0000000Z', 
    # 'time_open': '2021-05-16T00:00:00.0000000Z', 
    # 'time_close': '2021-05-16T00:00:00.0000000Z', 
    # 'rate_open': 46768.5467267036, 
    # 'rate_high': 46768.5467267036, 
    # 'rate_low': 46768.5467267036, 
    # 'rate_close': 46768.5467267036}