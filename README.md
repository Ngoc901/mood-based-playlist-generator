Popularity Prediction and Spotify Integration

Overview

This project implements a music popularity prediction system using machine learning techniques and integrates with the Spotify API to manage and analyze music playlists.

Features

Predicts song popularity using multiple regression models (Linear, Polynomial, Lasso, Ridge, Random Forest)

Retrieves song metadata from Spotify

Generates popularity-based insights with visualization

Searches for tracks and manages Spotify playlists

Technologies Used

Python: Programming language

NumPy, Pandas: Data manipulation

Matplotlib, Seaborn: Data visualization

Scikit-Learn: Machine learning models

Spotipy: Spotify Web API integration

Ollama: AI-based text processing

Installation

Clone the repository:

git clone https://github.com/your-repo-url.git
cd your-repo

Install dependencies:

pip install -r requirements.txt

Set up environment variables in a .env file:

SPOTIFY_CLIENT_ID=your-client-id
SPOTIFY_CLIENT_SECRET=your-client-secret
SPOTIFY_REDIRECT_URI=your-redirect-uri
SPOTIFY_PLAYLIST_NAME=your-playlist-name

Run the application:

python main.py

Usage

Predicting Song Popularity

The PopularityPrediction class takes a dataset containing song metadata and applies machine learning techniques to predict a song's popularity.

from PopularityPrediction import PopularityPrediction

prediction = PopularityPrediction()
df = client.get_track_properties(TRACKS)
prediction.popularity_prediction(df)

Interacting with Spotify

Searching for Tracks and Adding to Playlist

client = SpotifyClient()
client.add_to_playlist(TRACKS)

Generating a Bar Chart of Popularity

client.bar_chart()

AI-Powered Playlist Recommendation

from DS import get_tracks
tracks = get_tracks("Chill summer vibes")
print(tracks)

Machine Learning Models Implemented

Linear Regression

Polynomial Regression

Lasso Regression

Ridge Regression

Random Forest Regression

Data Preprocessing

Converts release_date to release_year

Converts categorical variables (explicit, album_type) into numeric format

One-hot encodes categorical features

Computes feature importance using correlation analysis