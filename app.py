
import re
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
import requests
import os
import pandas as pd
import plotly
import plotly.express as px
import json
import datetime
from datetime import date
from user import User
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient

from mongo_db import do_things, user_add, user_print, each_user_functions

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)


graph_holder = []
current_user_queries = []
global_user_id = []

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

login_manager = LoginManager()
login_manager.login_view = '/'
login_manager.init_app(app)

client = WebApplicationClient(GOOGLE_CLIENT_ID)

@login_manager.user_loader
def load_user(user_id):
    response = requests.get(f"https://djlmt-chartify.herokuapp.com/user/print/{user_id}")
    jsonified_data = json.loads(response.text)
    random_id = os.urandom(32)
    user = User(id_=random_id, name=jsonified_data["user_name"], email=jsonified_data["user_email"], profile_pic="")
    return user

@app.route("/", methods=['GET'])
def index():
    # args = request.args
    if current_user.is_authenticated:
        # return (
        #     "<p>Hello, {}! You're logged in! Email: {}</p>"
        #     "<div><p>Google Profile Picture:</p>"
        #     '<img src="{}" alt="Google profile pic"></img></div>'
        #     '<a class="button" href="/logout">Logout</a>'.format(
        #         current_user.name, current_user.email, current_user.profile_pic
        #     )
        # )
        return render_template('index.html',  user_name=current_user.name, user_email=current_user.email,
                               user_pic=current_user.profile_pic, user=current_user, graphJSON=graph_holder)
    else:
        # return '<a class="button" href="/login">Google Login</a>'

        #Args is a dictionary that contains key "requestJSON".  This is how we pass our graph data.
        # if args:
        #     if args["graphJSON"]:
        #         return render_template('index.html', graphJSON=args["graphJSON"])
        #

        return render_template('index.html', graphJSON=graph_holder, error_text=None)

# Below route is hit if user doesn't enter a coin name
@app.route('/api/')
def default():
        return redirect(url_for('index'))

@app.route('/api/<coin>', methods=["GET","POST"])
def get_coin_data(coin, time=100):
    coin = coin.upper()
    if request.method == "POST":
        coin_name = request.form.get("coin_name")
        timeframe = request.form.get("timeframe")
        print(f"Coin name: {coin_name}, timeframe: {timeframe}")
        # ALMOST working.... timeframe is being overwritten to 100 by our 'default' argument?
        return redirect(url_for('get_coin_data', coin=coin_name, time=timeframe))

    if coin in current_user_queries:
        pass
    else:
        if global_user_id:
            id = global_user_id[0]
        response = requests.get(f"https://djlmt-chartify.herokuapp.com/user/print/{id}")
        jsonified_data = json.loads(response.text)
        requests.put(f"https://djlmt-chartify.herokuapp.com/user/print/{id}/{coin}", json=jsonified_data)
        current_user_queries.append(coin)
    #Sets the end of our timeframe:
    ending_date = date.today()
    ending_time = "00:00:00"

    #Sets the start of our timeframe to be however many days prior to present:
    starting_date = ending_date - datetime.timedelta(time)

    #Construct API URL:
    base_url = 'https://rest.coinapi.io/v1/exchangerate/'
    COIN_API_KEY = os.getenv('COIN_API_KEY')
    headers = {'X-CoinAPI-Key': COIN_API_KEY}
    rest_of_query = f'/USD/history?period_id=1DAY&time_start={starting_date}T{ending_time}&time_end={ending_date}T{ending_time}'
    request_url = base_url + coin + rest_of_query


    # Error catching:
    try:
        response = requests.get(request_url, headers=headers)
    except:
        return render_template('index.html', graphJSON=graph_holder, error_text="❌ Could not contact API.")

    if response.status_code == 429:
        return render_template('index.html', graphJSON=graph_holder, error_text="❌ API rate limit reached. Please tell a dev.")

    data = response.json()

    try:
        df = pd.DataFrame(data)
        fig = px.line(df, x="time_period_end", y="rate_high", title=f"📈💸 Stonks for {coin} from {starting_date} to {ending_date}")
        # fig.update_layout(margin=dict(l=100, r=100, t=100, b=100))
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        graph_holder.append(graphJSON)

        return redirect(url_for('index'))

    except:
        return render_template('index.html', graphJSON=graph_holder, error_text="❌ Coin not found.")

    df = pd.DataFrame(data)
    fig = px.line(
        df, x="time_period_end", y="rate_high", 
        title=f"{coin} from {starting_date} to {ending_date}", template="plotly_dark", labels={
            "time_period_end":"Date",
            "rate_high":"Value ($)"}
        )
    fig.data[0].line.color = "#ffd700"
    fig.update_layout(paper_bgcolor="#303030")
    fig.update_layout(yaxis_tickformat=("~s,"))

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    graph_holder.append(graphJSON)
    return redirect(url_for('index'))


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400
    # Create a user in your db with the information provided
    # by Google
    active_user = {"user_name" : users_name, "user_email": users_email}
    active_id = requests.get("https://djlmt-chartify.herokuapp.com/users/ids", json=active_user)
    user_id = active_id.text
    global_user_id.append(active_id.text)
    user = User(id_=user_id, name=users_name, email=users_email, profile_pic=picture)

    response = requests.get(f"https://djlmt-chartify.herokuapp.com/user/print/{user_id}")
    jsonified_data = json.loads(response.text)
    user_queries = jsonified_data["user_queries"]
    list_format = user_queries.split(", ")
    
    for coin in list_format:
        requests.get(f"https://djlmt-chartify.herokuapp.com/api/{coin}")
    

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    graph_holder.clear()
    global_user_id.clear()
    current_user_queries.clear()
    return redirect("/")

@app.route('/users/ids')
def get_ids():
    user_id = do_things(request)
    return user_id

@app.route('/user/add', methods=["POST"])
def add_users():
    user_add(request)
    return make_response('', 200)

@app.route('/user/print/<user_id>', methods=["GET"])
def return_user(user_id):
    response = user_print(request, user_id)
    return response

@app.route('/user/print/<user_id>/<new_coin>', methods=["GET","PUT","DELETE"])
def other_functions(user_id, new_coin):
    each_user_functions(user_id, new_coin, request)
    return make_response('', 201)
