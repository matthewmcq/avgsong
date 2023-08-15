import billboardtops
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests
import uvicorn
import csv
import pandas as pd
import json

class Tracks:
    def __init__(self, track_id, album_id, artist, genres, name, headers) -> None:
        self.name = name
        self.headers = headers
        self.track_id = track_id
        self.album_id = album_id
        self.artist = artist
        self.genres = genres
        self.song_name = None

        self.acousticness = None
        self.danceability = None
        self.energy = None
        self.instrumentalness = None
        self.liveness = None
        self.loudness = None
        self.speechiness = None
        self.valence = None
        self.tempo = None
        self.key = None
        self.mode = None
        self.time_signature = None
        self.duration = None
        # Could add segments

    def get_audio_features(self):
        response = requests.get("https://api.spotify.com/v1/audio-features/" + self.track_id, headers=self.headers)
        audio_features = response.json()
        self.set_audio_features(audio_features)

    def set_audio_features(self, audio_features):
            try:
                self.acousticness = audio_features["acousticness"]
                self.energy = audio_features["energy"]
                self.instrumentalness = audio_features["instrumentalness"]
                self.liveness = audio_features["liveness"]
                self.loudness = audio_features["loudness"]
                self.speechiness = audio_features["speechiness"]
                self.valence = audio_features["valence"]
                self.tempo = audio_features["tempo"]
                self.key = audio_features["key"]
                self.mode = audio_features["mode"]
                self.time_signature = audio_features["time_signature"]
                self.duration = audio_features["duration_ms"]
            except:
                self.acousticness = None
                self.energy = None
                self.instrumentalness = None
                self.liveness = None
                self.loudness = None
                self.speechiness = None
                self.valence = None
                self.tempo = None
                self.key = None
                self.mode = None
                self.time_signature = None
                self.duration = None


class Albums:
    def __init__(self, album_id, headers) -> None:
        self.album_id = album_id
        self.headers = headers
        self.album_name = None
        self.artist = None
        self.artist_id = None
        self.genres = None
        self.tracks = []


    def get_album(self, response):
        response = requests.get("https://api.spotify.com/v1/albums/" + self.album_id, headers=self.headers)
        album = response.json()
        items = album["items"]
        self.set_album(album,items)



    def set_album(self, album, items):
        self.album_name = album["name"]
        print(self.album_name)
        self.artist = album["artists"][0]["name"]
        self.artist_id = album["artists"][0]["id"]
        self.get_genre()
        self.get_tracks(items)

    def get_tracks(self, tracks):
        #gets tracks from album all at once
        track_ids = []
        for track in tracks:
            track_ids.append(track["id"])
        response = requests.get("https://api.spotify.com/v1/audio-features/?ids=" + ",".join(track_ids), headers=self.headers)
        audio_features = response.json()["audio_features"]
        tracks_by_ids = requests.get("https://api.spotify.com/v1/tracks/?ids=" + ",".join(track_ids), headers=self.headers)
        for i in range(len(tracks)):
            track = Tracks(track_ids[i], self.album_id, self.artist, self.genres, None,  self.headers)
            track.set_audio_features(audio_features[i])
            track.name = tracks_by_ids.json()["tracks"][i]["name"]
            ###get genres
            track.genres = self.genres
            self.tracks.append(track)

    def get_genre(self):
        response = requests.get("https://api.spotify.com/v1/artists/" + self.artist_id, headers=self.headers)
        artist = response.json()
        try:
            self.genres = artist["genres"]
        except:
            self.genres = []


class Queries:
    def __init__(self, headers, years_dict):
        self.years_dict = years_dict
        self.headers = headers
        self.queries = {}
        self.album_ids_years = {}
        self.albums = {}

        for key in years_dict:
            self.queries[key] = []

        for year in years_dict:
            for album in years_dict[year]:
                album_to_find = album[1].replace(" ", "%20")
                artist = album[2].replace(" ", "%20")
                self.queries[year].append(f"https://api.spotify.com/v1/search?q=album%3A{album_to_find}%20artist%3A{artist}&type=album&market=US&limit=1&offset=0")

        print("initialized")
        self.get_album_ids_years()
        self.get_albums()
        #self.get_song_ids_years()
        
    #with open("album_ids.json", "r") as infile:
    #    album_ids_years = json.load(infile)

    def get_album_ids_years(self):
        #if self.album_ids_years != {} or self.album_ids_years is not None:
        #    return
        for year in self.queries:
            print(year)
            self.album_ids_years[year] = []
            for query in self.queries[year]:
                response = requests.get(query, headers=self.headers)
                if response.status_code == 200:
                    items = response.json()["albums"]["items"]
                    if len(items) > 0:
                        album_id = items[0]["id"]
                        print(album_id)
                        self.album_ids_years[year].append(album_id)
                else:  
                    print(response.status_code)
        with open("album_ids.json", "w") as outfile:
            json.dump(self.album_ids_years, outfile)
    

    def get_albums(self):
        for year in self.album_ids_years:
            self.albums[year] = []
            for i, album_id in enumerate(self.album_ids_years[year]):
                ### Get album 20 at a time
                if i % 20 == 0:
                    response = requests.get("https://api.spotify.com/v1/albums?ids=" + ",".join(self.album_ids_years[year][i:i+20]), headers=self.headers)
                    albums = response.json()
                    items = albums["albums"]
                    for item in items:
                        album_obj = Albums(item["id"], self.headers)
                        album_obj.set_album(item, item["tracks"]["items"])
                        self.albums[year].append(album_obj)
    
    def albums_to_csv(self):
        i = 0
        for year in self.albums:
            i = 1
            for album in self.albums[year]:
                for song in album.tracks:
                    with open("data.csv", "a", newline='') as csvfile:
                        writer = csv.writer(csvfile, delimiter=',')
                        writer.writerow([year, album.album_name, i, song.name, song.track_id, song.album_id, song.artist, song.genres, song.acousticness, song.danceability, song.energy, song.instrumentalness, song.liveness, song.loudness, song.speechiness, song.valence, song.tempo, song.key, song.mode, song.time_signature, song.duration])
                i += 1