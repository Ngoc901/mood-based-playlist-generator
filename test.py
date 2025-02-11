from ollama import chat
from ollama import ChatResponse
from SP import SpotifyClient
from DS import get_tracks

user_input = input("Enter your mood: ")
tracks = get_tracks(user_input)

client = SpotifyClient()
client.add_to_playlist(tracks)




