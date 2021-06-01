import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import datetime

from secrets import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

REDIRECT_URL = "http://localhost:8888/callback"



def access_api():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=REDIRECT_URL,
        scope="user-read-recently-played"
    ))
    return sp


def get_recently_played_tracks() -> pd.DataFrame:
    sp = access_api()
    today = datetime.datetime.now()
    ndays_ago = today - datetime.timedelta(days=7)  # 1 week
    time = int(ndays_ago.timestamp()) * 1000
    songs = sp.current_user_recently_played(after=time)
    song_dict = {
        "song_id": [],
        "song_name": [],
        "artist_id": [],
        "artist_name": [],
        "played_at": [],
        "timestamps": []
    }

    for song in songs['items']:
        song_dict['song_id'].append(song["track"]['id'])
        song_dict['song_name'].append(song["track"]["name"])
        song_dict['artist_id'].append(
            song["track"]["album"]["artists"][0]["id"])
        song_dict['artist_name'].append(
            song["track"]["album"]["artists"][0]["name"])
        song_dict['played_at'].append(song["played_at"])
        song_dict["timestamps"].append(song["played_at"][0:10])

    song_df = pd.DataFrame(song_dict)
    return song_df


def get_song_features(ids: str) -> pd.DataFrame:
    """
    :param ids:
    :return: 
    """
    sp = access_api()
    audio_features = sp.audio_features(tracks=ids)
    feature_dict = {
        "song_id": [],
        "danceability": [],
        "energy": [],
        "loudness": [],
        "speechiness": [],
        "acousticness": [],
        "instrumentalness": [],
        "liveness": [],
        "valence": [],
        "tempo": [],
    }
    for song in audio_features:
        feature_dict['song_id'].append(song['id'])
        feature_dict['danceability'].append(song['danceability'])
        feature_dict['energy'].append(song['energy'])
        feature_dict['loudness'].append(song['loudness'])
        feature_dict['speechiness'].append(song['speechiness'])
        feature_dict['acousticness'].append(song['acousticness'])
        feature_dict['instrumentalness'].append(song['instrumentalness'])
        feature_dict['liveness'].append(song['liveness'])
        feature_dict['valence'].append(song['valence'])
        feature_dict['tempo'].append(song['tempo'])

    return pd.DataFrame(feature_dict)


def get_artist_genres(id):
    sp = access_api()
    artist_json = sp.artist(artist_id=id)
    artist_id = artist_json['id']
    genres_list = artist_json['genres']
    genres_dic = {
        'artist_id': [],
        'genres': []
    }

    for genres in genres_list:
        genres_dic['artist_id'].append(artist_id)
        genres_dic['genres'].append(genres)

    return pd.DataFrame(genres_dic)


def get_artist(id):
    sp = access_api()
    artist_json = sp.artist(artist_id=id)
    artist_df = pd.DataFrame([{'artist_id': artist_json['id'],
                               'name': artist_json['name'],
                               'followers':artist_json['followers']['total'],
                               'popularity':artist_json['popularity'],
                               'genres':artist_json['genres']}])

    return artist_df


def get_songs(id):
    sp = access_api()
    songs_json = sp.track(track_id=id)
    songs_dict = {
        'song_id': [],
        'name' : [],
        'artist_id': [],
        'album_id': [],
        'popularity': [],
        'duration_ms': [],
        'external_urls': []
    }

    songs_dict['song_id'].append(songs_json['id'])
    songs_dict['name'].append(songs_json['name'])
    songs_dict['artist_id'].append(songs_json['artists'][0]['id'])
    songs_dict['album_id'].append(songs_json['album']['id'])
    songs_dict['popularity'].append(songs_json['popularity'])
    songs_dict['duration_ms'].append(songs_json['duration_ms'])
    songs_dict['external_urls'].append(songs_json['external_urls']['spotify'])

    return pd.DataFrame(songs_dict)