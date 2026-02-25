from datetime import date
import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()
API_KEY =  os.getenv('API_KEY')
CHANNEL_HANDLE = 'ariefmuhammaddd'
MAX_RESULTS = 50

class get_channel_data:
    
        def __init__(self, api_key: str = API_KEY):
            self.api_key = api_key

        def get_playlist_id(self, channel_handle: str = CHANNEL_HANDLE) -> str:
            """Get the playlist ID of a YouTube channel's uploads.
            
            Args:
                channel_handle: The id of the YouTube channel.
                api_key: The API key for the YouTube Data API.
            Returns:
                string: The playlist ID of the channel's uploads.
            """
            try:
                BASE_URL = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={channel_handle}&key={self.api_key}'
                response = requests.get(BASE_URL)
                response.raise_for_status()
                data = response.json()
                res = data["items"][0]["contentDetails"]["relatedPlaylists"]['uploads']
                return res
            except requests.exceptions.RequestException as e:
                raise e

        def get_video_ids(self, playlist_id: str, max_results: int = MAX_RESULTS) -> list:
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
            BASE_URL = f'https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={max_results}&playlistId={playlist_id}&key={self.api_key}'

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

        def extract_video_stats(self, video_ids: list) -> list:
            """Extract video statistics for a list of video ids.

            Args:
                video_ids (list): List of video ids to extract statistics for.
                api_key (str, optional): API key for YouTube Data API. Defaults to API_KEY.

            Returns:
                list: A list of dictionaries containing video statistics.
            """
            stats = []
            BASE_URL = f'https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&key={self.api_key}'
            
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
            
        def save_stats_to_json(self, stats: list, filename: str) -> None:
            """Save video statistics to a JSON file.

            Args:
                stats (list): A list of dictionaries containing video statistics.
                filename (str): The name of the JSON file to save the statistics to.
            """
            filepath = f'{filename}_{date.today()}.json'
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(stats, f, indent=4, ensure_ascii=False)
                    
            except IOError as e:
                raise e
            
            finally:
                print(f'Stats saved to {filepath}')

if __name__ == "__main__":
    main = get_channel_data()
    test = main.get_playlist_id()
    video_ids = main.get_video_ids(test)
    stats = main.extract_video_stats(video_ids)
    main.save_stats_to_json(stats, 'video_stats')