from SP import SpotifyClient

tracks = {
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


client = SpotifyClient()
client.add_to_playlist(tracks)
client.predict(tracks)
