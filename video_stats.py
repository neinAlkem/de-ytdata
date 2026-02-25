import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()
API_KEY =  os.getenv('API_KEY')
CHANNEL_HANDLE = 'ariefmuhammaddd'
MAX_RESULTS = 50

def get_playlist_id(channel_handle: str = CHANNEL_HANDLE, api_key: str = API_KEY) -> str:
    """Get the playlist ID of a YouTube channel's uploads.
    
    Args:
        channel_handle: The id of the YouTube channel.
        api_key: The API key for the YouTube Data API.
    Returns:
        string: The playlist ID of the channel's uploads.
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

def get_video_ids(playlist_id: str, api_key: str = API_KEY, max_results: int = MAX_RESULTS) -> list:
    """Get all video ids from playlist id

    Args:
        playlist_id (str): output from get_playlist_id function
        api_key (str, optional): API key for YouTube Data API. Defaults to API_KEY.
        max_results (int, optional): Maximum number of results to retrieve per API call. Defaults to MAX_RESULTS.
    Returns:
        list: list of video ids
    """
    video_ids = []
    pake_token = None
    BASE_URL = f'https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={max_results}&playlistId={playlist_id}&key={api_key}'

    try:
        while True:
            url = BASE_URL
            if pake_token:
                url += f'&pageToken={pake_token}'
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            for item in data.get('items', []):
                video_ids.append(item['contentDetails']['videoId'])
                
            page_token = data.get('nextPageToken')
            if not page_token:
                break
            pake_token = page_token
        return video_ids
    except requests.exceptions.RequestException as e:
        raise e

if __name__ == "__main__":
    test = get_playlist_id()
    print(get_video_ids(test))