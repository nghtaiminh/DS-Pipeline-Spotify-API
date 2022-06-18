import os 
from dotenv import load_dotenv, find_dotenv

import streamlit as st
from sqlalchemy import create_engine

from chart_utils import *
from db_utils import *

load_dotenv(find_dotenv())

HOST=os.environ['DB_HOST']
DATABASE=os.environ['DB_NAME']
USER=os.environ['DB_USERNAME']
PASSWORD=os.environ['DB_PASSWORD']

# Connect to PostgresSQL database
engine = create_engine('postgresql+psycopg2://{username}:{password}@{host}/{database}'.format(username=USER, 
                                                                                            password=PASSWORD,
                                                                                            host=HOST,
                                                                                            database=DATABASE))


#-----------------------------------------------------------
# Config
st.set_page_config(layout="wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


#-----------------------------------------------------------
# Visualizations
#-----------------------------------------------------------
st.title("Visualization of Your Listening History")

placeholder = st.empty()


with placeholder.container():
    stat1, stat2, stat3, stat4 = st.columns(4)

    stat1.metric(label="Total Plays 🎧", value= get_total_plays(engine))
    stat2.metric(label="Total Play Minutes ⌚", value=get_total_minutes(engine))
    stat3.metric(label="Saved Tracks 🎵", value=get_total_tracks(engine))
    stat4.metric(label="Saved Artists 👩‍🎤", value=get_total_artists(engine))

#-----------------------------------------------------------
# Top K 
st.header(" What is your most played songs and artists")
col11, col12 = st.columns(2)
with col11:
    st.plotly_chart(plot_top_songs(get_top_songs(engine)), use_container_width=True, height=500)     

with col12:
    st.plotly_chart(plot_top_artists(get_top_artists(engine)), use_container_width=True, height=500)      

#-----------------------------------------------------------
# Habits
st.header("What is your Spotify listening habits")
col21, col22 = st.columns(2)

with col21:
    st.plotly_chart(plot_plays_per_day(get_plays_per_day(engine)), use_container_width=True, height=500)

with col22:
    st.plotly_chart(plot_listetning_hour(get_distribution_of_listening_hour(engine)), use_container_width=True, height=500)

#-----------------------------------------------------------
# Tatses
st.header("What is your music tastes")
col31, col32 = st.columns(2)

with col31:
    st.plotly_chart(plot_song_popularity_chart(get_song_popularity(engine)) , use_container_width=True)

with col32:
    st.plotly_chart(plot_distribution_of_album_release_year(get_distribution_of_album_release_year(engine)), use_container_width=True)





