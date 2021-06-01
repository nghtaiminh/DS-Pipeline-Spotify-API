import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import datetime

from extract import get_recently_played_tracks, get_song_features, get_artist, get_songs


def check_played_songs_table(df: pd.DataFrame) -> pd.DataFrame:

    # Check empty
    if df.empty():
        print('No songs received from Spotify API!')



    # Check Dupplicate (One song can play multiple times)



    # Primary Check

def check_song_features_table(df: pd.DataFrame) -> pd.DataFrame:
    # Check Duplicate
    pass

def check_song_table(df: pd.DataFrame) -> pd.DataFrame:
    # Check Duplicate
    pass

def check_time_table(df: pd.DataFrame) -> pd.DataFrame:
    # Check TimeZone
    pass

def check_artist_table(df: pd.DataFrame) -> pd.DataFrame:
    # Check Duplicate
    pass
