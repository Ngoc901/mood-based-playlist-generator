import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import matplotlib.pyplot as plt
import webbrowser
import numpy as np
import pandas as pd


class SpotifyClient:
    def __init__(self):
        ## Loading environment variables
        load_dotenv()

        # Passing credentials and creating object of spotify( when you creating an object, you are establishing connection)
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
            redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
            scope="playlist-modify-private playlist-modify-public"
        ))

        # Here you are getting current users playlist
        playlists = self.sp.current_user_playlists()

        # Here you are loading the specific playlist
        self.target_playlist = next(p for p in playlists['items'] if p['name'] == os.getenv('SPOTIFY_PLAYLIST_NAME'))['id']
        self.target_playlist_link = next(p for p in playlists['items'] if p['name'] == os.getenv('SPOTIFY_PLAYLIST_NAME'))['external_urls']['spotify']


        self.x_chart = []
        self.y_chart = []

    def search_tracks(self, track_list):
        track_uris = []
        self.x_chart = []
        self.y_chart = []
        for track, artist in track_list.items():
            results = self.sp.search(q= 'track:' + track + ' artist:' + artist, type='track', limit=1)
            if bool(results['tracks']['items']):
                print(results['tracks']['items'][0]['uri'])
                track_uris.append(results['tracks']['items'][0]['uri'])
                self.x_chart.append(results['tracks']['items'][0]['name'])
                self.y_chart.append(results['tracks']['items'][0]['popularity'])
        return track_uris

    def add_to_playlist(self, track_list):
        uris = self.search_tracks(track_list)
        self.sp.playlist_replace_items(self.target_playlist, uris[:100])
        webbrowser.open_new(self.target_playlist_link)

    def bar_chart(self):
        plt.bar(self.x_chart, self.y_chart, color = "hotpink", width = 0.3)
        plt.title("Popularity of Recommended Songs")
        plt.xlabel("Artists")
        plt.ylabel("Popularity")
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.5)
        plt.show()

    # def print_playlist_link(self):
    #     for p in self.target_playlist_link:
    #         print(p)


    def get_playlist_link(self, playlist_name):
        results = self.sp.search(q=playlist_name, type="playlist", limit=1)

        if results['playlists']['items']:
            playlist = results['playlists']['items'][0]  # Get first match
            return playlist['external_urls']['spotify']  # Return Spotify link
        else:
            return "Playlist not found!"



    # def get_playlist_data(self, track_list):
    #     for track, artist in track_list.items():
    #         results = self.sp.search(q='track:' + track + ' artist:' + artist, type='track', limit=1)
    #         if bool(results['tracks']['items']) == True:
    #             return results
    # def circular_bar_plot(self, track_list):
    #
    #     # Build a dataset
    #     df = pd.DataFrame()
    #     df = pd.DataFrame(columns=['Artists', 'Duration'])
    #
    #
    #     for track, artist in track_list.items():
    #         results = self.sp.search(q='track:' + track + ' artist:' + artist, type='track', limit=1)
    #         if bool(results['tracks']['items']) == True:
    #             df.loc[len(df)] = [artist, results['tracks']['items'][0]['duration_ms']]
    #
    #     plt.figure(figsize=(20, 10))
    #     ax = plt.subplot(111, polar=True)
    #     plt.axis('off')
    #
    #     upperLimit = 100
    #     lowerLimit = 30
    #
    #     plt.figure(figsize=(20, 10))
    #     ax = plt.subplot(111, polar=True)
    #     plt.axis('off')
    #     upperLimit = 100
    #     lowerLimit = 30
    #
    #     max = df['Duration'].max()
    #
    #     slope = (max - lowerLimit) / max
    #     heights = slope * df['Duration'] + lowerLimit
    #
    #     # Compute the width of each bar. In total, we have 2*Pi = 360°
    #     width = 2 * np.pi / len(df.index)
    #
    #     # Compute the angle each bar is centered on:
    #     indexes = list(range(1, len(df.index) + 1))
    #     angles = [element * width for element in indexes]
    #
    #
    #     # Draw bars
    #     bars = ax.bar(
    #         x=angles,
    #         height=heights,
    #         width=width,
    #         bottom=lowerLimit,
    #         linewidth=2,
    #         edgecolor="white",
    #         color="hotpink")
    #
    #     # little space between the bar and the label
    #     labelPadding = 4
    #
    #     # Add labels
    #     for bar, angle, height, label in zip(bars, angles, heights, df["Duration"]):
    #
    #         # Labels are rotated. Rotation must be specified in degrees :(
    #         rotation = np.rad2deg(angle)
    #
    #         # Flip some labels upside down
    #         alignment = ""
    #         if angle >= np.pi / 2 and angle < 3 * np.pi / 2:
    #             alignment = "right"
    #             rotation = rotation + 180
    #         else:
    #             alignment = "left"
    #
    #         # Finally add the labels
    #         ax.text(
    #             x=angle,
    #             y=lowerLimit + bar.get_height() + labelPadding,
    #             s=label,
    #             ha=alignment,
    #             va='center',
    #             rotation=rotation,
    #             rotation_mode="anchor")
    #
    #
    #     plt.title("Duration of Recommended Songs (ms)")
    #     plt.show()

    # def predict(self, track_list):
    #     for track, artist in track_list.items():
    #         results = self.sp.search(q='track:' + track + ' artist:' + artist, type='track', limit=1)
    #         if bool(results['tracks']['items']) == True:
    #             track_data = results['tracks']['items']
    #
    #     data = {
    #         'popularity': track_data['popularity'],
    #         'release_year': int(track_data['album']['release_date'][:4]),  # Extract year
    #         'num_playlists': np.random.randint(10, 500),  # Placeholder for playlist count
    #     }
    #
    #     df = pd.DataFrame([data])
    #
    #     # Creating a simple model
    #     X = df[['release_year', 'num_playlists']]
    #     y = df['popularity']
    #
    #     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    #     model = LinearRegression()
    #     model.fit(X_train, y_train)
    #
    #     # Predict future popularity
    #     future_data = pd.DataFrame({'release_year': [2025], 'num_playlists': [300]})
    #     predicted_popularity = model.predict(future_data)
    #
    #     print(f"Predicted Popularity: {predicted_popularity[0]}")



