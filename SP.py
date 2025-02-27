# Access operating system functions, specifically for retrieving environment variables
# Allows sensitive credentials to be stored securely outside of the code
import os
# Load environment variables from .env file
# Keeps configuration and credentials seperated from code, improving security and flexibility
from dotenv import load_dotenv
# Interact with Spotify's Web API using OAuth for authentication
# Enables application to perform authorized operations
from spotipy.oauth2 import SpotifyOAuth
import spotipy
# Visualization for barchart
import matplotlib.pyplot as plt
# Open URLs in the default web browser
import webbrowser
# For data manipulation
import pandas as pd

# Defines a Spotify client that interacts with Spotify’s API (searching tracks, modifying playlists, visualizing popularity).


class SpotifyClient:
    # Sets up the Spotify connection and preloads the target playlist so that subsequent operations(searching tracks, adding tracks, visualization) have the necessary context and credentials.
    def __init__(self):
        # Loading environment variables, making them available with os.getenv
        # Keeping secrets separate from code
        load_dotenv()

        # Creates SpotifyOAuth instance using credentials (client ID, client secret, redirect URI) fetched from environment
        # Instantiates a Spotipy client for making API calls
        # Import the Oauth handler from spotipy
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv('SPOTIFY_CLIENT_ID'), # Fetches client ID
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'), # Fetches teh client secret
            redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'), # Sets the redirect URI
            # ensures you can modify both public and private playlists
            scope="playlist-modify-private playlist-modify-public"
        ))

        # Getting current user's playlists
        playlists = self.sp.current_user_playlists()

        # Finds the target playlist based on a name specified in the environment
        # Stores playlist ID
        self.target_playlist = next(p for p in playlists['items'] if p['name'] == os.getenv('SPOTIFY_PLAYLIST_NAME'))['id']
        # Stores public link
        self.target_playlist_link = next(p for p in playlists['items'] if p['name'] == os.getenv('SPOTIFY_PLAYLIST_NAME'))['external_urls']['spotify']

        # Initializes empty lists later for plotting
        self.x_chart = []
        self.y_chart = []

    def search_tracks(self, track_list):
        # Accepts a dictionary (track_list) where keys are track names and values are artist names
        track_uris = []
        self.x_chart = [] # Resets every time method is called
        self.y_chart = []
        # Constructing a query for each track and calls the Spotify search API
        for track, artist in track_list.items():
            # Construck a search query combining the track and artist name, limiting the results one
            results = self.sp.search(q= 'track:' + track + ' artist:' + artist, type='track', limit=1)
            # If the track is found, it prints and stores the track’s URI, and appends the track’s name and popularity to lists used for charting
            if bool(results['tracks']['items']):
                print(results['tracks']['items'][0]['uri'])
                track_uris.append(results['tracks']['items'][0]['uri'])
                self.x_chart.append(results['tracks']['items'][0]['name'])
                self.y_chart.append(results['tracks']['items'][0]['popularity'])
        return track_uris

    def get_track_properties(self, track_list):
        # Gather metadata for each track
        data = []
        for track, artist in track_list.items():
            results = self.sp.search(q='track:' + track + ' artist:' + artist, type='track', limit=1)
            if bool(results['tracks']['items']):
                track_info = {
                    'duration_ms': results['tracks']['items'][0]['duration_ms'],
                    'explicit': results['tracks']['items'][0]['explicit'],
                    'popularity': results['tracks']['items'][0]['popularity'],
                    'release_date': results['tracks']['items'][0]['album']['release_date'],
                    'total_tracks': results['tracks']['items'][0]['album']['total_tracks'],
                    'album_type': results['tracks']['items'][0]['album']['album_type'],

            }
            # Getting the popularity of the artist, by making an additional API call
            if bool(results['tracks']['items']):
                artist_id = results['tracks']['items'][0]['artists'][0]['id']
                artist_info = self.sp.artist(artist_id)
                artist_popularity = artist_info['popularity']
                track_info['popularity_of_artists'] = artist_popularity

            data.append(track_info)
            # All extracted data is appended as a dictionary to a list, which is finally converted to a Pandas DataFrame

        # Creating the DataFrame
        df = pd.DataFrame(data)
        return df


    def add_to_playlist(self, track_list):
        # Uses search_tracks to get the track URIs from the provided track list
        uris = self.search_tracks(track_list)
        # Replaces the items in the target playlist with the newly found tracks (up to 100 items)
        self.sp.playlist_replace_items(self.target_playlist, uris[:100])
        # Opens the playlist in the web browser using the stored link
        webbrowser.open_new(self.target_playlist_link)

    def bar_chart(self):
        # Configures chart elements
        plt.bar(self.x_chart, self.y_chart, color = "hotpink", width = 0.3)
        plt.title("Popularity of Recommended Songs")
        plt.xlabel("Artists")
        plt.ylabel("Popularity")
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.5)
        plt.show()





