import spotipy
from spotipy.oauth2 import SpotifyOAuth

from typing import List 

import pandas as pd
import datetime

from secrets import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

REDIRECT_URL = "http://localhost:8888/callback"



def access_api():
    """ Create a Client Authorization flow and get the token """
    
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=REDIRECT_URL,
        scope="user-read-recently-played"
    ))
    
    return sp


def get_recently_played_songs():
    """Get user's recently-played-tracks data and structure the data for PlayedSong Table"""

    sp = access_api()
    today = datetime.datetime.now()
    ndays_ago = today - datetime.timedelta(days=5)  
    time = int(ndays_ago.timestamp()) * 1000
    songs = sp.current_user_recently_played(after=time)
    song_dict = {
        "song_id": [],
        "song_name": [],
        "artist_id": [],
        "artist_name": [],
        "played_at": [],
    }

    for song in songs['items']:
        song_dict['song_id'].append(song["track"]['id'])
        song_dict['song_name'].append(song["track"]["name"])
        song_dict['artist_id'].append(song["track"]["album"]["artists"][0]["id"])
        song_dict['artist_name'].append(song["track"]["album"]["artists"][0]["name"])
        song_dict['played_at'].append(song["played_at"])

    song_df = pd.DataFrame(song_dict)
    return song_df



def get_audio_features(ids: List[str]) -> pd.DataFrame:
    """Get audio features data and structure AudioFeature Table
    
    Args:
        ids: input list of song ID
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


def get_artist_genres(id: str) -> pd.DataFrame:
    """Get artist's genres data """
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


def get_artists(ids: List(str)) -> pd.DataFrame:
    """ Get multiple artist data and structure Artist Table

    Args:
        ids: input artist ID
    """
    sp = access_api()

    artists_dict = {
        'artist_id': [],
        'artist_name': [],
        'followers': [],
        'popularity': [],
        'external_urls': []
    }

    for id in ids:
        artist = sp.artist(id)
        artists_dict['artist_id'].append(artist['id'])
        artists_dict['artist_name'].append(artist['name'])
        artists_dict['followers'].append(artist['followers']['total'])
        artists_dict['popularity'].append(artist['popularity'])
        artists_dict['external_urls'].append(artist['external_urls']['spotify'])

    return pd.DataFrame(artists_dict)


def get_songs(ids: List[str]) -> pd.DataFrame:
    """ Get multiple songs data and structure Songs Table

    Args:
        isd: input list of song ID 
    """
    sp = access_api()
    songs_json = sp.tracks(tracks=ids, market=None) # maximum 50 IDs
    songs_dict = {
        'song_id': [],
        'song_name' : [],
        'artist_id': [],
        'album_id': [],
        'duration_ms': [],
        'popularity': [],
        'external_urls': []
    }

    for song in songs_json['tracks']:
        songs_dict['song_id'].append(song['id'])
        songs_dict['song_name'].append(song['name'])
        songs_dict['artist_id'].append(song['artists'][0]['id'])
        songs_dict['album_id'].append(song['album']['id'])
        songs_dict['popularity'].append(song['popularity'])
        songs_dict['duration_ms'].append(song['duration_ms'])
        songs_dict['external_urls'].append(song['external_urls']['spotify'])

    return pd.DataFrame(songs_dict)

