#official-joke-api.appspot.com/random_joke
import billboardtops
from queries import Queries
#r1 = requests.get("http://official-joke-api.appspot.com/random_joke")
#print(r1)
#print(r1.json()["type"])
from fastapi.middleware.cors import CORSMiddleware

#Get secret key and make call to API
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
import requests
import uvicorn
import app_playlist
import app_optimized
import processing
import json
import urllib

client_id = "76b3fdfd1fa14dcaba99c20d2a9a6cd6" #"54d0f71b09ad478b8cc5647fbd3849b5" #"b858f069ec524253abe1015d52cfcc5d" #"15bbf420b29e47a6bf67e58a88423900" #"b858f069ec524253abe1015d52cfcc5d" #
client_secret = "c5e9073ecf3542a58cf256dba1eca527" # "4181692edccb4f39ad7da0c64b06933a" #"39401123204849138c685db0f4a6ef8a" #"5d7d9beffa564fa7aa41e505120b2882" #"39401123204849138c685db0f4a6ef8a"#
redirect_uri = "http://localhost:8000/callback"
# client_id = "YOUR_CLIENT_ID"
# client_secret = "YOUR_CLIENT_SECRET"
# redirect_uri = "YOUR_REDIRECT_URI" # e.g. http://localhost:8000/callback/ --> you will have to whitelist this url in the spotify developer dashboard 

app = FastAPI()

origins = [
    "http://localhost:3000",  # Allow frontend origin
    # "https://your.production.frontend.domain",  # You can also add your production frontend origin if needed
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def fetch_spotify_user_profile(headers):
    response = requests.get("https://api.spotify.com/v1/me", headers=headers)
    data = response.json()
    return data

def get_access_token(auth_code: str):
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": redirect_uri,
        },
        auth=(client_id, client_secret),
    )
    access_token = response.json()["access_token"]
    return {"Authorization": "Bearer " + access_token}

PROCESSED_DATA = {}

def process_data(headers, user_id):
    print("Processing data...")
    print
    #result = app_playlist.return_all_closest_as_json(headers)
    result = app_optimized.run_app(headers)
    print("Done processing data.")
    #print(result)
    result_json = urllib.parse.quote(json.dumps(result))
    #print(result_json)
    PROCESSED_DATA[user_id] = result_json



@app.get("/")
async def auth():
    scope = ["playlist-modify-private", "playlist-modify-public", "playlist-read-private", "playlist-read-collaborative"]
    auth_url = f"https://accounts.spotify.com/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={' '.join(scope)}"
    return RedirectResponse(url=auth_url) # Directly redirect to the Spotify authentication URL

@app.get("/callback")
async def callback(code: str, background_tasks: BackgroundTasks):
    headers = get_access_token(code)
    
    # Fetch the Spotify user profile
    user_data = fetch_spotify_user_profile(headers)
    
    # Extract unique user ID
    user_id = user_data['id']
    print(user_id)
    # Start the background task for data processing
    background_tasks.add_task(process_data, headers, user_id)

    # Redirect to the loading page, the user won't wait for processing
    # The unique user_id can be included in the redirect URL if needed later
    redirect_url = f'http://localhost:3000/loading?user_id={user_id}'
    return RedirectResponse(url=redirect_url, status_code=303)


@app.get("/checkData")
async def check_data(user_id: str):
    # Check if the data is ready for this specific user.
    if user_id in PROCESSED_DATA:
        return {
            "ready": True,
            "result": PROCESSED_DATA[user_id]
        }
    else:
        return {
            "ready": False
        }

def main():
    uvicorn.run(app)

if __name__ == "__main__":
    main()