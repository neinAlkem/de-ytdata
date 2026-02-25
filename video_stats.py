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

def extract_video_stats(video_ids: list, api_key: str = API_KEY) -> list:
    """Extract video statistics for a list of video ids.

    Args:
        video_ids (list): List of video ids to extract statistics for.
        api_key (str, optional): API key for YouTube Data API. Defaults to API_KEY.

    Returns:
        list: A list of dictionaries containing video statistics.
    """
    stats = []
    BASE_URL = f'https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id=FC53Ht_J1Tk&key={api_key}'
    
    def batch_video_ids(video_ids: list, batch_size: int) -> list:
        """Batch video ids into smaller lists.

        Args:
            video_ids (list): List of video ids to be batched.
            batch_size (int, optional): The size of each batch. Defaults to 50.

        Returns:
            list: A list of batches, where each batch is a list of video ids.
        """
        return [video_ids[i:i + batch_size] for i in range(0, len(video_ids), batch_size)]
        
    try:
        for batch in batch_video_ids(video_ids, MAX_RESULTS):
            video_ids_str = ','.join(batch)
            url = BASE_URL + f'&id={video_ids_str}'
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            for item in data.get('items',[]):
                video_id = item['id']
                snippet = item['snippet']
                content_details = item['contentDetails']
                statistic = item['statistics']
                
                video_data = {
                    'video_id' : video_id,
                    'title' : snippet['title'],
                    'published_at' : snippet['publishedAt'],
                    'duration' : content_details['duration'],
                    'view_count' : statistic.get('viewCount', 0),
                    'like_count' : statistic.get('likeCount', 0),
                    'comment_count' : statistic.get('commentCount', 0)
                }
                
                stats.append(video_data)
            
        return stats
    
    except requests.exceptions.RequestException as e:
        raise e

if __name__ == "__main__":
    test = get_playlist_id()
    video_ids = get_video_ids(test)
    extract_video_stats(video_ids)