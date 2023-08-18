import requests
import json

class Playlist:
    def __init__(self, headers, playlist_id) -> None:
        self.playlist_id = playlist_id
        self.headers = headers
        self.tracks = []
        self.audio_features = {
            'acousticness': 0, 'energy': 0, 'instrumentalness': 0,
            'liveness': 0, 'loudness': 0, 'speechiness': 0, 'tempo': 0, 
            'valence': 0, 'tempo': 0, 'key': 0, 'mode': 0, 
            'time_signature': 0, 'duration_ms': 0
        }
        self.genres = {}
        self.playlist_image = ""
        self.top_genres = []
        self.total_genre_count = 0
        self.top_song = ""
        self.tracks_to_score = {}
    
    def find_top_song(self):
        top_song = ""
        top_song_score = 0
        #print("Finding top song for playlist " + playlist.playlist_name)
        for track_id in self.tracks:
            feature_score = 0
            track_audio_features = track_ids_to_audio_features[track_id]
            track_genres = artist_ids_to_genres[track_ids_to_artists[track_id]]
            for feature in track_audio_features.keys():
                try:
                    normalized_difference = abs((track_audio_features[feature] - self.audio_features[feature]) / self.audio_features[feature] )
                    # print("Normalized difference for feature " + feature + " is " + str(normalized_difference))
                    feature_score += normalized_difference #maybe remove **2
                except:
                    print("Error getting audio feature " + feature)
                    continue
            #print("Feature score for track " + track_id + " is " + str(feature_score))
            genre_score = 0
            for genre in track_genres:
                if genre in self.genres:
                    genre_score += self.genres[genre]
            #print("Genre score for track " + track_id + " is " + str(genre_score))
            track_score =  genre_score / feature_score
            #print("Total score for track " + track_id + " is " + str(track_score))  
            self.tracks_to_score[track_id] = track_score
        #print("Top song for playlist " + playlist.playlist_name + " is " + top_song)
        top_song = max(self.tracks_to_score, key=self.tracks_to_score.get)
        self.top_song = top_song
        print("Top song for playlist " + self.playlist_name + " is " + track_ids_to_names[self.top_song])
        
track_ids_to_playlists = {}
track_ids_to_artists = {}
artist_ids_to_genres = {}
artist_ids_to_names = {}
artist_ids_to_track_ids = {}
track_ids_to_names = {}
track_ids_to_images = {}
track_ids_to_audio_features = {}
playlist_ids_to_playlist_objects = {}

### GET DATA ###

def get_user_playlists(headers: dict):
    response = requests.get("https://api.spotify.com/v1/me/playlists?limit=20", headers=headers)
    playlists = response.json()
    return playlists

def get_playlist_tracks(headers: dict, playlists_response: dict):
    playlists_to_process = []
    track_ids_to_find = set()
    playlist_ids = [playlist["id"] for playlist in playlists_response["items"]]
    print("Playlist ids: " + str(playlist_ids))
    for playlist_id in playlist_ids:
        print("Processing playlist " + playlist_id)
        this_playlist = Playlist(headers, playlist_id)
        response = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}", headers=headers)
        playlist = response.json()
        this_playlist.playlist_name = playlist["name"]
        try:
            this_playlist.playlist_image = playlist["images"][0]["url"]
        except: 
            this_playlist.playlist_image = ""
        tracks_response = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=headers)
        try:
            tracks = tracks_response.json()["items"]
            if len(tracks) < 5:
                continue
            track_ids = [track["track"]["id"] for track in tracks]
            for track_id in track_ids:
                this_playlist.tracks.append(track_id)
                if track_id not in track_ids_to_playlists:
                    track_ids_to_playlists[track_id] = set()
                track_ids_to_playlists[track_id].add(playlist_id)
                track_ids_to_find.add(track_id)
        except:
            print("Error getting tracks for playlist" + playlist_id)
            continue
        playlist_ids_to_playlist_objects[playlist_id] = this_playlist
        playlists_to_process.append(this_playlist)
    return playlists_to_process, track_ids_to_find

def find_track_info(headers: dict, track_ids_to_find: set):
    # Change so returns artist_ids to find
    # Max 50 at a time
    tracks_to_find = ""
    track_ids_to_find = list(track_ids_to_find)
    artist_ids_to_find = set()
    for i in range(0, len(track_ids_to_find), 50): #Check if this is the right way to do this
        tracks_to_find = ",".join(track_ids_to_find[i:i+50])
        response = requests.get(f"https://api.spotify.com/v1/tracks?ids={tracks_to_find}", headers=headers)
        tracks = response.json()["tracks"] 
        for track in tracks:
            try:
                # Get the track id
                track_id = track["id"]
                # Get the track name
                track_name = track["name"]
                # Get the track image
                track_image = track["album"]["images"][0]["url"]
                # Add it to the track_ids_to_names hashmap
                track_ids_to_names[track_id] = track_name
                #print(track_name)
                # Add it to the track_ids_to_images hashmap
                track_ids_to_images[track_id] = track_image
                # Get the artist id
                artist_id = track["album"]["artists"][0]["id"]
                # Add it to the artist_ids_to_track_ids hashmap
                if artist_id not in artist_ids_to_track_ids:
                    artist_ids_to_track_ids[artist_id] = []
                artist_ids_to_track_ids[artist_id].append(track_id)
                # Add it to the artist_ids_to_find set
                artist_ids_to_find.add(artist_id)
                # Add the artist to the track_ids_to_artists hashmap
                track_ids_to_artists[track_id] = artist_id
            except:
                print("Error getting track info")
                continue
    return artist_ids_to_find

def find_artist_info(headers: dict, artist_ids_to_find: set):
    # Max 50 at a time
    artists_to_find = ""
    artist_ids_to_find = list(artist_ids_to_find)
    for i in range(0, len(artist_ids_to_find), 50): #Check if this is the right way to do this
        artists_to_find = ",".join(artist_ids_to_find[i:i+50])
        response = requests.get(f"https://api.spotify.com/v1/artists?ids={artists_to_find}", headers=headers)
        artists = response.json()["artists"] 
        for artist in artists:
            try:
                # Get the artist id
                artist_id = artist["id"]
                # Get the artist name
                artist_name = artist["name"]
                # Add it to the artist_ids_to_names hashmap
                artist_ids_to_names[artist_id] = artist_name
                # Get the artist genres
                artist_genres = artist["genres"]
                # Add it to the artist_ids_to_genres hashmap
                artist_ids_to_genres[artist_id] = artist_genres
            except:
                print("Error getting artist info")
                continue

def find_audio_features(headers: dict, track_ids_to_find: set):
    # Max 100 at a time:
    tracks_to_find = ""
    track_ids_to_find = list(track_ids_to_find)
    for i in range(0, len(track_ids_to_find), 100): 
        tracks_to_find = ",".join(track_ids_to_find[i:i+100])
        response = requests.get(f"https://api.spotify.com/v1/audio-features?ids={tracks_to_find}", headers=headers)
        audio_features = response.json()["audio_features"]
        to_add = {'acousticness' : 0,  'energy': 0, 'instrumentalness': 0, 'liveness': 0, 'loudness': 0, 'speechiness': 0, 'tempo': 0, 'valence': 0, 'tempo': 0, 'key' : 0, 'mode' : 0, 'time_signature' : 0, 'duration_ms': 0}

        for feature in audio_features:
            features_to_add = {}
            # Get the track id
            track_id = feature["id"]
            # Add it to the track_ids_to_audio_features hashmap
            for key in feature.keys():
                if key in to_add:
                    features_to_add[key] = feature[key]
            track_ids_to_audio_features[track_id] = features_to_add
            
### PROCESS DATA ###

def process_playlists(playlists):
    """Should calculate all the genre info and playlist audio features by iterating through the track_ids_to_playlists hashmap"""
    for playlist in playlists:
        #print(playlist.tracks)
        for track_id in playlist.tracks:
            track_audio_features = track_ids_to_audio_features[track_id]
            track_genres = artist_ids_to_genres[track_ids_to_artists[track_id]]
            for genre in track_genres:
                #print(genre)
                # Add the genre to the playlist
                if genre not in playlist.genres:
                    playlist.genres[genre] = 0
                playlist.genres[genre] += 1
                # Add the audio features to the playlist
            for key in track_audio_features:
                playlist.audio_features[key] += track_audio_features[key]
        # Divide the audio features by the number of tracks in the playlist
        for genre in playlist.genres:
            playlist.genres[genre] /= len(playlist.genres)
        for key in playlist.audio_features:
            playlist.audio_features[key] /= len(playlist.tracks)
        playlist.total_genre_count = len(playlist.tracks)
        playlist.top_genres = sorted(playlist.genres, key=playlist.genres.get, reverse=True)[:3]
    return playlists
        
def normalize_audio_features():
    """Should normalize the audio features of all songs"""
    max_audio_features = {
            'acousticness': 0, 'energy': 0, 'instrumentalness': 0,
            'liveness': 0, 'loudness': 0, 'speechiness': 0, 'tempo': 0, 
            'valence': 0, 'tempo': 0, 'key': 0, 'mode': 0, 
            'time_signature': 0, 'duration_ms': 0
        }
    min_audio_features = {
            'acousticness': 0, 'energy': 0, 'instrumentalness': 0,
            'liveness': 0, 'loudness': 0, 'speechiness': 0, 'tempo': 0, 
            'valence': 0, 'tempo': 0, 'key': 0, 'mode': 0, 
            'time_signature': 0, 'duration_ms': 0
        }
    for track_id in track_ids_to_audio_features.keys():
        track_audio_features = track_ids_to_audio_features[track_id]
        for feature in track_audio_features.keys():
            if track_audio_features[feature] > max_audio_features[feature]:
                max_audio_features[feature] = track_audio_features[feature]
            if track_audio_features[feature] < min_audio_features[feature]:
                min_audio_features[feature] = track_audio_features[feature]

    for track_id in track_ids_to_audio_features.keys():
        track_audio_features = track_ids_to_audio_features[track_id]
        for feature in track_audio_features.keys():
            track_ids_to_audio_features[track_id][feature] = (track_audio_features[feature] - min_audio_features[feature]) / (max_audio_features[feature] - min_audio_features[feature])
            print(track_ids_to_audio_features[track_id][feature])

### RETURN DATA ###

def run_app(headers):
    playlist_response = get_user_playlists(headers)
    print("got user playlists")
    if playlist_response == None:
        print("Error getting user playlists")
        return None  
    playlists, track_ids_to_find  = get_playlist_tracks(headers, playlist_response)
    artist_ids_to_find = find_track_info(headers, track_ids_to_find)
    find_artist_info(headers, artist_ids_to_find)
    find_audio_features(headers, track_ids_to_find)
    normalize_audio_features()
    playlists = process_playlists(playlists)
    ret = []
    #print(playlist_ids_to_playlist_objects.keys())
    for playlist in playlists:
            playlist.find_top_song()
            #print("Top song for playlist " + playlist.playlist_name + " is " + playlist.top_song)
            if playlist.top_song == None:
                continue
            #print("Top song for playlist " + playlist.playlist_name + " is " + playlist.top_song)
            ret.append({
                "playlist_name": playlist.playlist_name,
                "song_name": track_ids_to_names[playlist.top_song],
                "artist": artist_ids_to_names[track_ids_to_artists[playlist.top_song]],
                "top_track_image": track_ids_to_images[playlist.top_song],
                "image_url": playlist.playlist_image,
                "playlist_genre_count": playlist.total_genre_count,
                # This might error:
                "playlist_top_genres": json.dumps(playlist.top_genres),
            })
            print(track_ids_to_names[playlist.top_song])  
    return ret