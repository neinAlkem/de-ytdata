import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()
API_KEY =  os.getenv('API_KEY')
CHANNEL_HANDLE = 'ariefmuhammaddd'

def get_playlist_id(channel_handle: str = API_KEY, api_key: str = API_KEY) -> str:
    try:
        BASE_URL = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={channel_handle}&key={api_key}'
        response = requests.get(BASE_URL)
        response.raise_for_status()
        data = response.json()
        res = data["items"][0]["contentDetails"]["relatedPlaylists"]['uploads']
        return res
    except requests.exceptions.RequestException as e:
        raise e

if __name__ == "__main__":
    get_playlist_id()
