import psycopg2
import pandas as pd


#-----------------------------------------------------------
# Funcitons
def get_total_plays(conn):
    query = """
        SELECT
            COUNT(played_song_id)
        FROM played_song
        WHERE played_at >= date_trunc('month', current_date - interval '1' month);
    """

    try:
        result = pd.read_sql_query(query, con=conn)
    except psycopg2.DatabaseError as e:
        print(f'Query failed!\n\n{e}')

    return result['count']

def get_total_minutes(conn):
    query = """
		SELECT
			(SUM(s.duration_ms) / 60000) as minute
        FROM played_song p, Song s
        WHERE played_at >= date_trunc('month', current_date - interval '1' month)
            AND p.song_id = s.song_id;
    """

    try:
        result = pd.read_sql_query(query, con=conn)
    except psycopg2.DatabaseError as e:
        print(f'Query failed!\n\n{e}')

    return result['minute']

def get_total_tracks(conn):
    query = """
        SELECT 
            COUNT(*) AS total_tracks
        FROM song;
    """

    try:
        result = pd.read_sql_query(query, con=conn)
    except psycopg2.DatabaseError as e:
        print(f'Query failed!\n\n{e}')

    return result['total_tracks']

def get_total_artists(conn):
    query = """
        SELECT 
            COUNT(*) AS total_artists
        FROM artist;
    """

    try:
        result = pd.read_sql_query(query, con=conn)
    except psycopg2.DatabaseError as e:
        print(f'Query failed!\n\n{e}')

    return result['total_artists']

def get_plays_per_day(conn):
    plays_per_day = pd.read_sql("""
        SELECT 
            DATE(dt),
            COALESCE(count_plays, 0) AS count
        FROM generate_series(CURRENT_DATE - interval '1' MONTH, CURRENT_DATE, '1 day'::INTERVAL) dt 
        LEFT JOIN (
            SELECT
                DATE(played_at) AS dt,
                COUNT(played_song_id) AS count_plays
            FROM played_song
            WHERE played_at >= DATE_TRUNC('month', CURRENT_DATE - interval '1' MONTH)
            GROUP BY DATE(played_at)
        ) c USING(dt)
    """, con=conn)

    return plays_per_day


def get_song_popularity(conn):
    query = """
        SELECT 
            song_name,
            popularity,
            count,
            external_url
        FROM song
        LEFT JOIN (
            SELECT 
                song_id, COUNT(played_song_id)
            FROM played_song
            GROUP BY song_id
        ) AS play_count ON play_count.song_id = song.song_id;
    """

    try:
        result = pd.read_sql_query(query, con=conn)
    except psycopg2.DatabaseError as e:
        print(f'Query failed!\n\n{e}')

    return result


def get_album_popularity(conn):
    query = """
        SELECT 
            album.album_name,
            popularity,
            count,
            external_url
        FROM album
        LEFT JOIN (
            SELECT
                album_id, COUNT(played_song_id)
            FROM played_song
            GROUP BY album_id
        ) AS album_count ON album_count.album_id = album.album_id;
    """
    try:
        result = pd.read_sql_query(query, con=conn)
    except psycopg2.DatabaseError as e:
        print(f'Query failed!\n\n{e}')

    return result

def get_distribution_of_album_release_year(conn):
    query = """
        SELECT 
            a.release_year,
            COUNT(*)
        FROM album a
        GROUP BY a.release_year
    """
    try:
        result = pd.read_sql_query(query, con=conn)
    except psycopg2.DatabaseError as e:
        print(f'Query failed!\n\n{e}')

    return result

def get_top_songs(conn, n=10):
    query = f"""
        SELECT
            s.song_name, 
            s.external_url,
            COUNT(p.played_song_id)
        FROM song s, played_song p
        WHERE  p.played_at > date_trunc('month', current_date - interval '1' month) AND p.song_id = s.song_id
        GROUP BY s.song_id
        ORDER BY 3 DESC
        LIMIT {n};
    """
    try:
        result =pd.read_sql(query, con=conn)
    except psycopg2.DatabaseError as e:
        print(f'Query failed!\n\n{e}')

    return result

def get_top_artists(conn, n=10):
    query = f"""
        WITH fre_artist_listen AS (
            SELECT 
                artist_id,
                COUNT(*)
            FROM played_song p
            FULL JOIN song_artists sa 
            ON p.song_id = sa.song_id
            GROUP BY artist_id)

        SELECT 
            artist_name,
            count,
            external_url
        FROM fre_artist_listen
        LEFT JOIN artist
        ON fre_artist_listen.artist_id = artist.artist_id
        ORDER BY count DESC
        LIMIT {n};
    """
    try:
        result =pd.read_sql(query, con=conn)
    except psycopg2.DatabaseError as e:
        print(f'Query failed!\n\n{e}')

    return result


def get_distribution_of_listening_hour(conn):
    query = """
        SELECT
            EXTRACT(HOUR FROM time.time::TIME)::NUMERIC AS hour,
            COUNT(start_time)
        FROM time
        GROUP BY hour;
    """
    try:
        result = pd.read_sql_query(query, con=conn)
    except psycopg2.DatabaseError as e:
        print(f'Query failed!\n\n{e}')

    return result