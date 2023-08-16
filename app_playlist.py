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
    playlist_id = None
    playlist_name = None
    image = None

    def __init__(self, headers, playlist_id) -> None:
        self.headers = headers
        self.playlist_id = playlist_id

    def get_name(self):
        response = requests.get("https://api.spotify.com/v1/playlists/" + self.playlist_id, headers=self.headers)
        playlist = response.json()
        self.playlist_name = playlist["name"]
        ## Also gets image:
        try:
            self.image = playlist["images"][0]["url"]
        except:
            self.image = "https://www.freeiconspng.com/uploads/no-image-icon-4.png"
        return playlist["name"]

    def closest_song_to_avg(self):
        if self.Tracks != []:
            return self.Tracks[0]


class TracksPlaylist(Tracks):
    genre_weighting = 0
    feature_weighting = 0
    overall_weighting = 0
    audio_features = {}
    def set_audio_features(self, audio_features):
        self.audio_features = audio_features
        return super().set_audio_features(audio_features)


def get_multiple_audio_features(track_ids, headers):
    response = requests.get("https://api.spotify.com/v1/audio-features/?ids=" + ",".join(track_ids), headers=headers)
    audio_features = response.json()
    res = {track_id : {} for track_id in track_ids}
    for i in range(len(track_ids)):
        res[track_ids[i]] = audio_features["audio_features"][i]
    return res

def set_multiple_audio_features(tracks, audio_features):
    for i in range(len(tracks)):
        tracks[i].set_audio_features(audio_features[i])
    return tracks

# Get users playlists:

def get_playlists(headers):
    #Limit=3 playlists for testing
    response = requests.get("https://api.spotify.com/v1/me/playlists?limit=3", headers=headers)
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
    playlist_names = [playlist["name"] for playlist in playlists["items"]]
    playlists = []
    for i in range(len(playlist_ids)):
        playlist = PlaylistAPI(headers, playlist_ids[i])
        playlist.get_name()
        playlist.Tracks = process_playlist(headers, playlist_ids[i])
        playlists.append(playlist)
    return playlists
    
def process_playlist(headers, playlist_id):
    print("Processing playlist: " + playlist_id)
    tracks = get_tracks(playlist_id, headers)
    track_ids = [track["track"]["id"] for track in tracks["items"]]
    track_artist_ids = [track["track"]["artists"][0]["id"] for track in tracks["items"]]
    track_audio_features = {}
    # get_multiple_audio_features for 100 tracks at a time
    for i in range(0, len(track_ids), 100):
        track_audio_features.update(get_multiple_audio_features(track_ids[i:i+100], headers))
    track_genres = [get_genres(artist_id, headers) for artist_id in track_artist_ids]
    tracks_lst = []
    for i in range(len(track_ids)):
        try:
            track = TracksPlaylist(track_ids[i], None, None, track_genres[i], None, headers)
            track.set_audio_features(track_audio_features[track_ids[i]])
            track.genres = track_genres[i]
            tracks_lst.append(track)
        except:
            continue
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
        weight += (track.audio_features[feature] - avg_features[feature])**2
    track.feature_weighting = weight
    #print(weight)
    return weight

def find_closest(playlist):
    #playlists = collect_data(playlist.headers)
    average_features = avg_features(playlist.Tracks)
    #print(average_features)
    genre_weights = weight_genres(playlist.Tracks)
    for track in playlist.Tracks:
        genre_weighting(track, genre_weights)
        feature_weighting(track, average_features)
        try:
            track.overall_weighting = track.genre_weighting * 1 / track.feature_weighting
        except: 
            track.overall_weighting = 0
    playlist.Tracks.sort(key=lambda x: x.overall_weighting, reverse=True)
    playlist.Tracks[0].song_name = find_name(playlist.Tracks[0].track_id, playlist.headers)
    playlist.Tracks[0].artist = find_artist(playlist.Tracks[0].track_id, playlist.headers)
    print("Closest for " + playlist.playlist_name + ": " + playlist.Tracks[0].song_name + " by " + playlist.Tracks[0].artist)
    return playlist

def find_name(track_id, headers):
    response = requests.get("https://api.spotify.com/v1/tracks/" + track_id, headers=headers)
    track_name = response.json()["name"]
    return track_name

def find_artist(track_id, headers):
    response = requests.get("https://api.spotify.com/v1/tracks/" + track_id, headers=headers)
    track_artist = response.json()["artists"][0]["name"]
    return track_artist

def find_all_closest(headers):
    print("Collecting data...")
    playlists = collect_data(headers)
    for playlist in playlists:
        print("Finding closest song for " + playlist.playlist_name + "...")
        playlist = find_closest(playlist)
    return playlists

def print_all_closest(headers):
    playlists = find_all_closest(headers)
    ret = ''
    for playlist in playlists:
        ret += "Playlist: " + playlist.playlist_name + " - Avg Song: " + playlist.Tracks[0].song_name + " by " + playlist.Tracks[0].artist + '\n'
    return ret

def return_all_closest_as_json(headers):
    playlists = find_all_closest(headers)
    ret = []
    for playlist in playlists:
        ret.append({
            "playlist_name": playlist.playlist_name,
            "song_name": playlist.Tracks[0].song_name,
            "artist": playlist.Tracks[0].artist,
            "image_url": playlist.image
        })
    return ret