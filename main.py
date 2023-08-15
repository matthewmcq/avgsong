#official-joke-api.appspot.com/random_joke
import billboardtops
from queries import Queries
#r1 = requests.get("http://official-joke-api.appspot.com/random_joke")
#print(r1)
#print(r1.json()["type"])


#Get secret key and make call to API
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests
import uvicorn
import app_playlist

client_id = "b858f069ec524253abe1015d52cfcc5d" #"15bbf420b29e47a6bf67e58a88423900"
client_secret = "39401123204849138c685db0f4a6ef8a" #"5d7d9beffa564fa7aa41e505120b2882"
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
    
    #years_dict = billboardtops.get_years_all() 
    #data = Queries(headers, years_dict)                # <-- REQUESTS ARE MADE HERE
    #data.albums_to_csv()
    #return HTMLResponse(content=f'<h1>Success!</h1>')
    top_songs = app_playlist.print_all_closest(headers)
    return HTMLResponse(content=f'<h1>Success!</h1><p>{top_songs}</p>')



def main():
    uvicorn.run(app)

if __name__ == "__main__":
    main()


