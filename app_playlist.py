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
        
    def playlist_genres(self):
        genres = {}
        for track in self.Tracks:
            for genre in track.genres:
                if genre in genres:
                    genres[genre] += 1
                else:
                    genres[genre] = 1
        return genres

class TracksPlaylist(Tracks):
    genre_weighting = 0
    feature_weighting = 0
    overall_weighting = 0
    audio_features = {}
    album_image = None

    def set_audio_features(self, audio_features):
        self.audio_features = audio_features
        return super().set_audio_features(audio_features)
    
    def set_album_image(self, image):
        self.album_image = image


def get_track_album_image(track_id, headers):
    response = requests.get("https://api.spotify.com/v1/tracks/" + track_id, headers=headers)
    track = response.json()
    try:
        return track["album"]["images"][0]["url"]
    except:
        return "https://www.freeiconspng.com/uploads/no-image-icon-4.png"

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
    #Limit=10 
    # Garrett userID: https://open.spotify.com/user/31sq5dyzdr5apb5d7hyykzamiyfa?si=fte4a4mHQw6R-B8ogG4WXw
    # Jack's: https://open.spotify.com/user/g0xuwxjyl18djkmqbhxdxz8mt?si=18118da361b24751
    # /user/31sq5dyzdr5apb5d7hyykzamiyfa
    # response_jack = requests.get("https://api.spotify.com/v1/users/g0xuwxjyl18djkmqbhxdxz8mt/playlists?limit=4", headers=headers)
    # response = requests.get("https://api.spotify.com/v1/users/31sq5dyzdr5apb5d7hyykzamiyfa/playlists?limit=4", headers=headers) # Garrett
    response = requests.get("https://api.spotify.com/v1/me/playlists?limit=10", headers=headers)
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
    playlist_num_tracks = [playlist["tracks"]["total"] for playlist in playlists["items"]]
    playlists = []
    for i in range(len(playlist_ids)):
        if playlist_names[i] == "Liked Songs":
            continue
        # If playlist is fewer than three songs, skip it
        if playlist_num_tracks[i] < 3:
            continue
        playlist = PlaylistAPI(headers, playlist_ids[i])
        playlist.get_name()
        playlist.Tracks = process_playlist(headers, playlist_ids[i])
        if playlist.Tracks != []:
            playlists.append(playlist)
    return playlists
    
def process_playlist(headers, playlist_id):
    print("Processing playlist: " + playlist_id)
    tracks = get_tracks(playlist_id, headers)
    if not tracks:
        return []
    if not tracks["items"]:
        return []
    
    try:
        track_ids = [track["track"]["id"] for track in tracks["items"]]
        track_artist_ids = [track["track"]["artists"][0]["id"] for track in tracks["items"]]
    except:
        return []
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
        weight += genre_weights[genre] 
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
    playlist.genre_weights = genre_weights
    for track in playlist.Tracks:
        genre_weighting(track, genre_weights)
        feature_weighting(track, average_features)
        try:
            track.overall_weighting = track.genre_weighting * 1 / track.feature_weighting
        except: 
            track.overall_weighting = 0
    # try:
    playlist.Tracks.sort(key=lambda x: x.overall_weighting, reverse=True)
    playlist.Tracks[0].song_name = find_name(playlist.Tracks[0].track_id, playlist.headers)
    playlist.Tracks[0].artist = find_artist(playlist.Tracks[0].track_id, playlist.headers)
    print("Closest for " + playlist.playlist_name + ": " + playlist.Tracks[0].song_name + " by " + playlist.Tracks[0].artist)
    return playlist
    # except:
    #     return playlist

def find_name(track_id, headers):
        response = requests.get("https://api.spotify.com/v1/tracks/" + track_id, headers=headers)
        try:
            track_name = response.json()["name"]
        except:
            print("Error finding name for track: " + track_id)
            track_name = track_id
        return track_name 
        
def find_artist(track_id, headers):
    response = requests.get("https://api.spotify.com/v1/tracks/" + track_id, headers=headers)
    try:
        track_artist = response.json()["artists"][0]["name"]
    except:
        print("Error finding artist for track: " + track_id)
        try:
            
            track_artist = response.json()["name"]
        except:
            print("Error again")
            track_artist = track_id
    return track_artist

def find_all_closest(headers):
    print("Collecting data...")
    playlists = collect_data(headers)
    for playlist in playlists:
        print("Finding closest song for " + playlist.playlist_name + "...")
        playlist = find_closest(playlist)
        if not playlist.Tracks[0].song_name:
            print("No song name for " + playlist.playlist_name)
            playlists.remove(playlist)
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
        #This could be optimized and done during weight genres
        if not playlist.Tracks[0].song_name:
            print("No song name for " + playlist.playlist_name)
            continue
        if not playlist.genre_weights:
            print("No genre weights for " + playlist.playlist_name)
            continue
        genres_to_copy = playlist.genre_weights
        genres = genres_to_copy.copy()
        ### Top three genres: 
        max_genres = []
        total_genre_count = len(genres)
        for i in range(3):
            max_genres.append(max(genres, key=genres.get))
            genres.pop(max_genres[i])
        total_genre_count = len(genres)
        ret.append({
            "playlist_name": playlist.playlist_name,
            "song_name": playlist.Tracks[0].song_name,
            "artist": playlist.Tracks[0].artist,
            "top_track_image": get_track_album_image(playlist.Tracks[0].track_id, headers),
            "image_url": playlist.image,
            "playlist_genre_count": total_genre_count,
            "playlist_top_genres": json.dumps(max_genres)
        })
        print(total_genre_count)
    return ret

    # Optimization plans to minimizae calls to spotify API:
    # Get all the playlists at once, then make dict of track_ids to look up and map them to the playlist(s) they belong to
    # make a dict of artist IDs to get genres for, then make a call to get all the genres for all the artists at once(?)
    # get audio features for as many tracks as possible at once and make another hashmap with track_ids -> audio features
    # Hashmaps (can clean up):
    # track_ids -> playlist(s)
    # track_ids -> artist_ids
    # artist_ids -> genres
    # artist_ids -> atrist_names
    # track_ids -> audio features
    # Then change process tracks to go trough something like:
    # for tracks in dict:
    #   for playlist in track_id in track_ids -> playlist(s):
    #       genres = artist_ids -> genres
    #       add genres to that playlists playlist_genres dict and increment as necessary
    #       add audio features to that playlists playlist_audio_features total and increment as necessary
    #       add track to that playlists playlist_tracks
    # Then go through each playlist and calculate the average audio features / len(tracks) and genre weights
    # Then go through tracks to find closest song and sort playlist.tracks to find closest song
    # Then get song name (GET request) and artist name from hashmap

    """ 
        New functions (DATA RETRIEVAL) TODO: 
        First: needs a get_playlists function that returns the JSON of all a users playlists (do this separate so the analyze function TODO can be called on it when times come sto make that)
        Second: Keep track of playlist_image (hashmap?), then find all track_ids + artist_ids (50 at a time, might need to use next page) (if not in hashmap already) for all playlists and make a hashmap of track_ids -> playlist(s) and track_ids -> artist_ids (same call) - (ignore a playlist if fewer than 10 songs)
        Third: Get genres + artist names (max 50 per call) for all artists not in dict and make a hashmap of artist_ids -> genres and artist_ids -> artist_names
        (DATA PROCESSING) TODO:
        Go through each track in track_id dict and add it to corresponding playlist.tracks, add its audio features to that of the playlist, 
            increment total genres, and add its genres to that of the playlist vis a vie the artist_ids -> genres hashmap
        Go through each playlist and calculate the average audio features / len(tracks) and genre weights (genres[genre]/total_genres) (during genre weights can calso calculate top 3 genres)
        Go through tracks to find closest song and sort playlist.tracks to find closest song
        Get song name + image url (GET request) and artist name from hashmap
        (SENDING DATA): TODO
        Send back playlist name, closest song name, closest song artist, playlist image, genre count, and top 3 genres as JSON
            """