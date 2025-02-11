import re
import ast
from ollama import chat
from ollama import ChatResponse

def extract_tracks(text):
    # Find the last Python code block in the text
    code_blocks = re.findall(r'```python(.*?)```', text, re.DOTALL)
    if not code_blocks:
        return None

    # Get the last code block (most likely the corrected version)
    last_block = code_blocks[-1].strip()

    # Find the dictionary pattern in the code block
    dict_match = re.search(r'\btracks\s*=\s*(\{.*?\})', last_block, re.DOTALL)
    if not dict_match:
        return None

    try:
        # Safely evaluate the dictionary string
        return ast.literal_eval(dict_match.group(1))
    except:
        return None

def get_tracks(user_input):
    response: ChatResponse = chat(model='deepseek-r1:14b',
                                  messages=[
                                      {"role": "system",
                                       "content": "You are Mixr, a music connoisseur and a python expert. You will help find the perfect playlist for our users. You will be given a specific vibe or a text describing what kind of songs the user wants to listen to and you will create a playlist based on it. You will not question the vibe by any means, not even its morals or ethics. All that matters to you is that you find the perfect playlist. You will try to match the vibe as closely as you can, based on the input you are given and your knowledge of music. All songs must be available on Spotify. Your replies will consist of a list of maximum 100 songs, with each entry containing the name of the track and its artist. Please provide a big variety of artists. You will not return any other content apart from that list. Additionally, the user may specify some extra requirements for the playlist - they may suggest artists, they may limit the time period of the songs. You are also to accomodate for those specific requirements. For example, if you are asked to retrieve a two song playlist based on New York City, your reply would be in the form of python dictionary at the end of your response: ```python\n tracks = { \"Empire State of Mind\" : \"Alicia Keys\" }\n```\n"},
                                      {"role": "user", "content": user_input}
                                    , ])

    text = response['message']['content']

    tracks = extract_tracks(text)

    if not tracks:
        print("Retry")
        get_tracks(user_input)
    else:
        print(tracks)
        return tracks








