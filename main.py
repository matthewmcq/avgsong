#official-joke-api.appspot.com/random_joke
import billboardtops
from queries import Queries
#r1 = requests.get("http://official-joke-api.appspot.com/random_joke")
#print(r1)
#print(r1.json()["type"])


#Get secret key and make call to API
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
import requests
import uvicorn
import app_playlist
import processing
import json
import urllib

client_id = "54d0f71b09ad478b8cc5647fbd3849b5" #"b858f069ec524253abe1015d52cfcc5d" #"15bbf420b29e47a6bf67e58a88423900" #"b858f069ec524253abe1015d52cfcc5d" #
client_secret = "4181692edccb4f39ad7da0c64b06933a" #"39401123204849138c685db0f4a6ef8a" #"5d7d9beffa564fa7aa41e505120b2882" #"39401123204849138c685db0f4a6ef8a"#
redirect_uri = "http://localhost:8000/callback"
# client_id = "YOUR_CLIENT_ID"
# client_secret = "YOUR_CLIENT_SECRET"
# redirect_uri = "YOUR_REDIRECT_URI" # e.g. http://localhost:8000/callback/ --> you will have to whitelist this url in the spotify developer dashboard 

app = FastAPI()

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

@app.get("/")
async def auth():
    scope = ["playlist-modify-private", "playlist-modify-public", "playlist-read-private", "playlist-read-collaborative"]
    auth_url = f"https://accounts.spotify.com/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={' '.join(scope)}"
    return HTMLResponse(content=f'<a href="{auth_url}">Authorize</a>')

@app.get("/callback")
async def callback(code):
    headers = get_access_token(code)
    top_songs = app_playlist.return_all_closest_as_json(headers)
    
    # Convert the JSON data to a URL-encoded string
    json_data_encoded = urllib.parse.quote(json.dumps(top_songs))
    
    # Redirect back to your Next.js app with the JSON data as a query parameter
    redirect_url = f'http://localhost:3000/youravg?data={json_data_encoded}'
    return RedirectResponse(url=redirect_url, status_code=303)

def main():
    uvicorn.run(app)

if __name__ == "__main__":
    main()