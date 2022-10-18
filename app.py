import os
from flask import Flask, render_template, redirect, request, session, make_response, session, redirect
import requests
import spotipy

from main import main

# Authentication Steps, paramaters, and responses are defined at https://developer.spotify.com/web-api/authorization-guide/
# Visit this url to see all the steps, parameters, and expected response.


app = Flask(__name__)
app.secret_key = "app_sec_key2"

API_BASE = 'https://accounts.spotify.com'

#  Client Keys
CLIENT_ID = os.environ['SPOTIPY_CLIENT_ID']
CLIENT_SECRET = os.environ['SPOTIPY_CLIENT_SECRET']

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)
# authorization-code-flow Step 1. Have your application request authorization;
# the user logs in and authorizes access
SCOPE = "playlist-modify-private,user-top-read"
REDIRECT_URI = "http://127.0.0.1:5000/api_callback"


@app.route("/")
def verify():
    session.clear()

    auth_url = f'{API_BASE}/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}'
    print(auth_url)
    return redirect(auth_url)


@app.route("/index")
def index():
    return render_template("index.html")

# authorization-code-flow Step 2.
# Have your application request refresh and access tokens;
# Spotify returns access and refresh tokens


@app.route("/api_callback")
def api_callback():
    session.clear()
    code = request.args.get('code')

    auth_token_url = f"{API_BASE}/api/token"
    res = requests.post(auth_token_url, data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    })

    res_body = res.json()
    print(res.json())
    session["toke"] = res_body.get("access_token")

    return redirect("index")


# authorization-code-flow Step 3.
# Use the access token to access the Spotify Web API;
# Spotify returns requested data
@app.route("/gen", methods=['GET'])
def gen():
    sp = spotipy.Spotify(auth=session['toke'])
    main(sp=sp)
    return render_template("gen.html")


if __name__ == "__main__":
    app.run(debug=True)
