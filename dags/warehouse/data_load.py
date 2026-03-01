import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def load_path() :
    file_path = f'.data/video_stats_{datetime.now().strftime("%Y%m%d%H%M%S")}.json'
    
    try: 
        logger.info(f'Processing video statistics data from API response, file: {file_path}')
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            logger.info(f'Successfully loaded video statistics data from file: {file_path}')
            return data

    except FileNotFoundError:
        logger.error(f'File not found: {file_path}')
        raise
   
    except json.JSONDecodeError:
        logger.error(f'Invalid JSON format in file: {file_path}')
        raise
   