import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import datetime
import numpy as np
from sqlalchemy import create_engine

from spotify_api import  get_songs, get_recently_played_songs, get_artists, get_audio_features
from secrets import HOST, DATABASE, USER, PASSWORD



if __name__ == "__main__":
    print("Start ETL process...")

    ##########################################################
    #      Extract 
    ##########################################################
    
    # Get recently played songs data
    played_songs_df = get_recently_played_songs()
    # Check recently-played songs empty
    if played_songs_df.empty:
        raise Exception("No songs found. Finished ETL process")

    # Get list of song ID without duplicate 
    song_ids_list = played_songs_df['song_id'].unique().tolist()
    # Get list of artist ID without duplicate 
    artist_ids_list = played_songs_df['artist_id'].unique().tolist()
    # Get timestamp
    timestamp_df = pd.to_datetime(played_songs_df['played_at'])
    # Get songs data
    songs_df = get_songs(song_ids_list)
    # Get songs features data
    audio_features_df = get_audio_features(song_ids_list)
    # Get artists data
    artists_df = get_artists(artist_ids_list)
    
    print("Data extracted, proceed to Transform stage")


    ##########################################################
    #      TRANSFORM 
    ##########################################################
    

    # Check missing values
    if played_songs_df.isnull().values.any():
        raise Exception("Null value found in played songs data")

    if songs_df.isnull().values.any():
        raise Exception("Null value found in songs data")

    if audio_features_df.isnull().values.any():
        raise Exception("Null value found in song feature data")

    if artists_df.isnull().values.any():
        raise Exception("Null value found in artist data")


    # SongsPlayed Table 
    # Change to GMT+7:00 timezone
    timestamp_df = timestamp_df + datetime.timedelta(hours=-5)
    #Set UNIX code for played_at as primary key, since only one song can played at a time
    played_songs_table_pk = timestamp_df.astype(np.int64) // 10**6
    # Format the timestamp
    timestamp_df = timestamp_df.dt.strftime("%m-%d-%Y %H:%M:%S")
    played_songs_df['played_at'] = timestamp_df
    played_songs_df.insert(0, "played_song_id", played_songs_table_pk)




    # Time Dimension Table
    played_songs_df['played_at'] = pd.to_datetime(played_songs_df['played_at'])
    time_df = pd.DataFrame({"start_time": played_songs_df['played_at'],
                                "time": played_songs_df['played_at'].astype(str).str[11:],
                                "day": played_songs_df['played_at'].dt.day,
                                "month": played_songs_df['played_at'].dt.month,
                                "year": played_songs_df['played_at'].dt.year,
                                "weekday": played_songs_df['played_at'].dt.weekday})

    print("Data is validated, proceed to Load stage")


    ##########################################################
    #      LOAD 
    ##########################################################


    engine = create_engine('postgresql+psycopg2://{username}:{password}@{host}/{database}'.format(username=USER, 
                                                                                                    password=PASSWORD,
                                                                                                    host=HOST,
                                                                                                    database=DATABASE))
    conn = engine.raw_connection()
    cur = conn.cursor()

    # Load data in temporary tables 

    # Song Table
    cur.execute('''
        CREATE TEMP TABLE IF NOT EXISTS temp_songs AS 
        SELECT * FROM Songs LIMIT 0;
    ''')
    songs_df.to_sql("temp_songs", con=engine, if_exists='replace', index=False)

    engine.execute('''
        INSERT INTO public.Songs
        SELECT * FROM temp_songs
        WHERE temp_songs.song_id NOT IN (SELECT song_id FROM public.Songs);
    ''')


    # Artist Table
    cur.execute('''
        CREATE TEMP TABLE IF NOT EXISTS temp_artists AS 
        SELECT * FROM Artists LIMIT 0;
    ''')
    artists_df.to_sql("temp_artists", con=engine, schema='public', if_exists='replace', index=False)
    engine.execute('''
        INSERT INTO public.Artists
        SELECT * FROM temp_artists
        WHERE temp_artists.artist_id NOT IN (SELECT artist_id FROM public.Artists);
    ''')


    # Time Table
    cur.execute('''
        CREATE TEMP TABLE IF NOT EXISTS temp_time AS 
        SELECT * FROM Time LIMIT 0;
    ''')
    time_df.to_sql("temp_time", con=engine, schema='public', if_exists='replace', index=False)
    engine.execute('''
        INSERT INTO public.Time
        SELECT * FROM temp_time
        WHERE temp_time.start_time NOT IN (SELECT start_time FROM public.Time);
    ''')


    # AudioFeatures Table
    cur.execute('''
        CREATE TEMP TABLE IF NOT EXISTS temp_audio_features AS 
        SELECT * FROM AudioFeatures LIMIT 0;
    ''')
    audio_features_df.to_sql("temp_audio_features", con=engine, if_exists='replace', index=False)
    engine.execute('''
        INSERT INTO public.AudioFeatures
        SELECT * FROM temp_audio_features
        WHERE temp_audio_features.song_id NOT IN (SELECT song_id FROM public.AudioFeatures);
    ''')


    # PlayedSongs Table
    cur.execute('''
        CREATE TEMP TABLE IF NOT EXISTS temp_played_songs 
        AS SELECT * FROM PlayedSongs LIMIT 0;
    ''')
    played_songs_df.to_sql("temp_played_songs", con=engine, if_exists='replace', index=False)

    engine.execute('''
        INSERT INTO public.PlayedSongs
        SELECT * FROM temp_played_songs
        WHERE CAST(temp_played_songs.played_song_id AS TEXT) NOT IN (SELECT played_song_id FROM public.PlayedSongs);
    ''')



    # Close connection
    cur.close()
    conn.close()

    print('ETL process finished!')




