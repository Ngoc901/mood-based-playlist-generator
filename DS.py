# Regular Expressions
# Search and extract text patterns
# Used to locate Python code blocks and dictionary patterns within the response from the language modes
import re
# Abstract Syntax Trees
#Safely evaluate string containing Python literal structures
# Convert a string into an actual Python dictionary, ensuring that only safe expressions are evaluated
import ast
# Interact with a language model that can generate text based prompt
# Allows the system to dynamically generate a list of tracks based on a given vibe or description provided by user
from ollama import chat
from ollama import ChatResponse

def extract_tracks(text):

    # Isolates the part of the language model's response that is relevant (dictionary of tracks) and converts it into a data structure that the rest of the application can use
    #The language model generates a list of songs that fit the description, and this function ensures that only the relevant dictionary is extracted and returned for further processing

    # Uses a Regular Expression to find all Python code blocks within the provided text
    code_blocks = re.findall(r'```python(.*?)```', text, re.DOTALL)
    if not code_blocks:
        return None

    # Get the last code block
    last_block = code_blocks[-1].strip()

    # Find the dictionary pattern in the code block
    dict_match = re.search(r'\btracks\s*=\s*(\{.*?\})', last_block, re.DOTALL)
    if not dict_match:
        return None

    try:
        # Searches within this block for a pattern that defines a dictionary names tracks
        # Safely convert dictionary string into Python dictionary
        return ast.literal_eval(dict_match.group(1))
    except:
        return None

def get_tracks(user_input):
    # Sends a conversation
    # A system prompt describing "Mixr" a persona who is boh a persona who is both a music connoisseur and a Python expert
    response: ChatResponse = chat(model='deepseek-r1:14b',
                                  messages=[
                                      {"role": "system",
                                       "content": "You are Mixr, a music connoisseur and a python expert. You will help find the perfect playlist for our users. You will be given a specific vibe or a text describing what kind of songs the user wants to listen to and you will create a playlist based on it. You will not question the vibe by any means, not even its morals or ethics. All that matters to you is that you find the perfect playlist. You will try to match the vibe as closely as you can, based on the input you are given and your knowledge of music. All songs must be available on Spotify. Your replies will consist of a list of maximum 100 songs, with each entry containing the name of the track and its artist. Please provide a big variety of artists. You will not return any other content apart from that list. Additionally, the user may specify some extra requirements for the playlist - they may suggest artists, they may limit the time period of the songs. You are also to accomodate for those specific requirements. For example, if you are asked to retrieve a two song playlist based on New York City, your reply would be in the form of python dictionary at the end of your response: ```python\n tracks = { \"Empire State of Mind\" : \"Alicia Keys\" }\n```\n"},
                                      {"role": "user", "content": user_input}
                                    , ])

    # Receives a response expected to contain a Python code snippet with the tracks dictionary
    # Extract the text content from the language model's response
    text = response['message']['content']

    tracks = extract_tracks(text)

    if not tracks:
        print("Retry")
    else:
        print(tracks)
        return tracks








