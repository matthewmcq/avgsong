from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests
import uvicorn
import csv
import pandas as pd
import json
from queries import Tracks

class PlaylistAPI():
    Tracks = []
    headers = None
    def __init__(self, headers) -> None:
        self.headers = headers

class TracksPlaylist(Tracks):
    genre_weighting = 0
    feature_weighting = 0
    overall_weighting = 0
    audio_features = {}
    def set_audio_features(self, audio_features):
        self.audio_features = audio_features
        return super().set_audio_features(audio_features)

# Get users playlists:

def get_playlists(headers):
    response = requests.get("https://api.spotify.com/v1/me/playlists", headers=headers)
    playlists = response.json()
    return playlists

# Get tracks from playlist:

def get_tracks(playlist_id, headers):
    response = requests.get("https://api.spotify.com/v1/playlists/" + playlist_id + "/tracks", headers=headers)
    tracks = response.json()
    return tracks

# Get audio features from tracks:

def get_audio_features(track_id, headers):
    try:
        response = requests.get("https://api.spotify.com/v1/audio-features/" + track_id, headers=headers)
        audio_features = response.json()
    except:
        audio_features = {}
    return audio_features

# Get genres from artists:

def get_genres(artist_id, headers):
    try:
        response = requests.get("https://api.spotify.com/v1/artists/" + artist_id, headers=headers)
        genres = response.json()["genres"]
    except:
        genres = []
    return genres

# Collect data:

def collect_data(headers):
    playlists = get_playlists(headers)
    playlist_ids = [playlist["id"] for playlist in playlists["items"]]
    return playlist_ids
    
def process_playlist(headers, playlist_id):
    tracks = get_tracks(playlist_id, headers)
    track_ids = [track["track"]["id"] for track in tracks["items"]]
    track_names = [track["track"]["name"] for track in tracks["items"]]
    track_artists = [track["track"]["artists"][0]["name"] for track in tracks["items"]]
    track_artist_ids = [track["track"]["artists"][0]["id"] for track in tracks["items"]]
    track_audio_features = [get_audio_features(track_id, headers) for track_id in track_ids]
    track_genres = [get_genres(artist_id, headers) for artist_id in track_artist_ids]
    tracks_lst = []
    for i in range(len(track_ids)):
        track = TracksPlaylist(track_ids[i], None, track_artists[i], track_genres[i], None, headers)
        track.set_audio_features(track_audio_features[i])
        track.name = track_names[i]
        track.genres = track_genres[i]
        tracks_lst.append(track)
    return tracks_lst

def normalize_features(tracks):
    min_features = dict()
    max_features = dict()
    for track in tracks:
        for feature in track.audio_features:
            if feature not in min_features:
                min_features[feature] = track.audio_features[feature]
                max_features[feature] = track.audio_features[feature]
            else:
                min_features[feature] = min(min_features[feature], track.audio_features[feature])
                max_features[feature] = max(max_features[feature], track.audio_features[feature])
    for track in tracks:
        for feature in track.audio_features:
            try:
                track.audio_features[feature] = (track.audio_features[feature] - min_features[feature]) / (max_features[feature] - min_features[feature])
            except: track.audio_features[feature] = 0

def avg_features(tracks):
    normalize_features(tracks)
    avg_features = dict()
    for track in tracks:
        for feature in track.audio_features:
            if feature not in avg_features:
                avg_features[feature] = track.audio_features[feature]
            else:
                avg_features[feature] += track.audio_features[feature]
    for feature in avg_features:
        avg_features[feature] /= len(tracks)
    return avg_features

# Weight genres by prevalence in playlist:

def weight_genres(tracks):
    genre_weights = dict()
    for track in tracks:
        for genre in track.genres:
            if genre not in genre_weights:
                genre_weights[genre] = 1
            else:
                genre_weights[genre] += 1
    for genre in genre_weights:
        genre_weights[genre] /= len(tracks)
    return genre_weights

def genre_weighting(track, genre_weights):
    weight = 0
    for genre in track.genres:
        weight += genre_weights[genre] / len(track.genres)
    track.genre_weighting = weight
    return weight

# Weight audio features by closeness to average of playlist:

def feature_weighting(track, avg_features):
    weight = 0
    for feature in track.audio_features:
        weight += abs(track.audio_features[feature] - avg_features[feature])
    track.feature_weighting = weight
    print(weight)
    return weight

def find_closest(headers):
    playlist = PlaylistAPI(headers)
    playlist_ids = collect_data(headers)
    playlist.Tracks = process_playlist(headers, playlist_ids[3])
    print(playlist.Tracks)
    average_features = avg_features(playlist.Tracks)
    print(average_features)
    genre_weights = weight_genres(playlist.Tracks)
    for track in playlist.Tracks:
        genre_weighting(track, genre_weights)
        feature_weighting(track, average_features)
        try:
            track.overall_weighting = track.genre_weighting * 1 / track.feature_weighting
        except: 
            track.overall_weighting = 0
    playlist.Tracks.sort(key=lambda x: x.overall_weighting, reverse=True)
    return playlist.Tracks

def find_name(track_id, headers):
    response = requests.get("https://api.spotify.com/v1/tracks/" + track_id, headers=headers)
    track_name = response.json()["name"]
    return track_name

