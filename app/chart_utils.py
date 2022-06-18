import pandas as pd

import plotly.express as px
import plotly.graph_objects as go


def plot_plays_per_day(data: pd.DataFrame):
    fig = px.line(data,
        x = data['date'], 
        y = data['count'],
        title = "Number of playbacks in the last 30 days",
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Number of playbacks"
    )

    return fig


def plot_top_songs(data: pd.DataFrame):
    fig = px.bar(data, 
                x="count",
                y="song_name",
                title="Top Songs", 
                orientation='h')

    fig.update_layout(
        yaxis={
            'categoryorder':'total ascending',
        },
        xaxis_title="Number of playbacks",
        yaxis_title="Song Name"
    )
    return fig

def plot_top_artists(data: pd.DataFrame):
    fig = px.bar(data, 
                x="count",
                title="Top Artist", 
                orientation='h')

    fig.update_layout(
        yaxis={
        'categoryorder':'total ascending',
        },
        xaxis_title="Number of playbacks",
        yaxis_title="Artists Name"
    )
    return fig

def  plot_song_popularity_chart(data: pd.DataFrame):
    fig = px.scatter(data, 
                        x="count", 
                        y="popularity", 
                        hover_data=["song_name"], 
                        title="What are the popularity of songs you listen to on Spotify")

    fig.update_layout(
        xaxis_title="Numbers of playbacks",
        yaxis_title="Polularity"
    )   
    return fig

def  plot_album_popularity_chart(data: pd.DataFrame):
    fig = px.scatter(data, 
                        x="count", 
                        y="popularity", 
                        hover_data=["album_name"])

    return fig

def plot_distribution_of_album_release_year(data: pd.DataFrame):
    fig = px.pie(data, 
                    values="count", 
                    names="release_year", 
                    title="What the release years of your listened albums")

    return fig

def plot_listetning_hour(data: pd.DataFrame):
    fig = px.bar(data, 
                    x="hour", 
                    y="count", 
                    title = "What time of a day you usually listene to? (From 0 to 24 hours)")

    fig.update_xaxes(range=[0,24])

    fig.update_layout(
        xaxis_title="Time of the day",
        yaxis_title="Number of playbacks"
    )

    return fig


