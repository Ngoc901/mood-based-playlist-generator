import requests

#
# # Example Usage
# songs = {
#     "Super Shy": "NewJeans",
#     "Eve, Psyche & The Bluebeard’s wife": "LE SSERAFIM",
#     "I AM": "IVE"
# }

from ollama import chat
from ollama import ChatResponse
from SP import SpotifyClient
from DS import get_tracks






#user_input = input("Enter your mood: ")
#tracks = get_tracks(user_input)

TRACKS = {
"Spring Day": "BTS",
"Through the Night": "IU",
"Sing for You": "EXO",
"Fine": "Taeyeon",
"You Were Beautiful": "DAY6",
"Light Years Away": "G.E.M.",
"Empty": "WINNER",
"I Need Somebody": "DAY6",
"Breathe": "Lee Hi",
"Lonely": "Jonghyun",
"How Have You Been?": "Eric Chou",
"If You": "BIGBANG",
"Time Spent Walking Through Memories": "Nell",
"Blue": "BOL4",
"Hug Me": "IZ*ONE",
"Eyes, Nose, Lips": "Taeyang",
"Goodbye": "Whee In",
"Rain": "TAEYEON",
"I Miss You": "MAMAMOO",
"Lonely Night": "Kwon Jin Ah",
"Through the Rain": "Kris Wu",
"Miracles in December": "EXO",
"Love Scenario": "iKON",
"Ending Scene": "IU",
"Let Me Out": "NU'EST",
"Lonely": "SISTAR",
"The Truth Untold": "BTS",
"Hello, Goodbye": "Hyolyn",
"Hurt": "EXO",
"I Will Go to You Like the First Snow": "Ailee",
"Missing You": "BTOB",
"Lonely": "2NE1",
"Starlight": "TAEYEON",
"Dear Moon": "JEON MI DO",
"Say Something": "TWICE",
}




if __name__ == "__main__":
    # user_input = input("Enter your mood: ")
    # tracks = get_tracks(user_input)
    client = SpotifyClient()
    client.add_to_playlist(TRACKS)
    client.bar_chart()
