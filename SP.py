import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
import spotipy

class SpotifyClient:
    def __init__(self):
        load_dotenv()
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
            redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
            scope="playlist-modify-private playlist-modify-public"
        ))
        playlists = self.sp.current_user_playlists()
        self.target_playlist = next(p for p in playlists['items'] if p['name'] == os.getenv('SPOTIFY_PLAYLIST_NAME'))['id']

    def search_tracks(self, track_list):
        track_uris = []
        for track, artist in track_list.items():
            results = self.sp.search(q= 'track:' + track + ' artist:' + artist, type='track', limit=1)
            if bool(results['tracks']['items']) == True:
                print(results['tracks']['items'][0]['uri'])
                track_uris.append(results['tracks']['items'][0]['uri'])
        return track_uris

    def add_to_playlist(self, track_list):
        uris = self.search_tracks(track_list)
        self.sp.playlist_replace_items(self.target_playlist, uris[:100])








