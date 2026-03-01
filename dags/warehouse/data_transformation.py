from datetime import timedelta, datetime
import re

def parse_duration(duration_str: str) -> timedelta:
    pattern = re.compile(
        r'P'
        r'(?:(\d+)D)?'
        r'T?'
        r'(?:(\d+)H)?'
        r'(?:(\d+)M)?'
        r'(?:(\d+)S)?'
    )
    
    match = pattern.match(duration_str)
    if not match:
        raise ValueError("Invalid duration format")
    
    days = int(match.group(1)) if match.group(1) else 0
    hours = int(match.group(2)) if match.group(2) else 0
    minutes = int(match.group(3)) if match.group(3) else 0
    seconds = int(match.group(4)) if match.group(4) else 0
    
    return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

def transform_data(row) :
    duration_td = parse_duration(row['duration'])
    row['duration'] = (datetime.min + duration_td).time()
    row['video_type'] = 'Short Video' if duration_td < timedelta(minutes=1) else 'Normal Video'
    
    return row