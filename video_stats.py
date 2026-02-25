import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()
API_KEY =  os.getenv('API_KEY')
CHANNEL_HANDLE = 'ariefmuhammaddd'

def get_playlist_id(channel_handle: str = CHANNEL_HANDLE, api_key: str = API_KEY) -> str:
    """Get the playlist ID of a YouTube channel's uploads.
    
    Args:
        channel_handle: The id of the YouTube channel.
        api_key: The API key for the YouTube Data API.
    Returns:
        The playlist ID of the channel's uploads.
    """
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
    test = get_playlist_id()