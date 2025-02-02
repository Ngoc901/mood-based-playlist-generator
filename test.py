from SP import SpotifyClient
tracks = {
    "Super Shy": "NewJeans",
    "Eve, Psyche & The Bluebeard’s wife": "LE SSERAFIM",
    "I AM": "IVE",
    "ASAP" : "NewJeans",
    "Attention": "NewJeans",
    "Hurt" : "NewJeans",
    "Cookie" : "NewJeans"

}
client = SpotifyClient()
client.add_to_playlist(tracks)
