"""
utility functions that can be reused, are defined here
"""
from datetime import datetime
import pytz
import os

# set the timezone as a constant here
LOCAL_TIMEZONE = 'Pacific/Auckland'


def get_timestamp():
    """
    Returns a formatted timestamp for files and folders
    """
    local_tz = pytz.timezone(LOCAL_TIMEZONE)
    return datetime.now(local_tz).strftime('%Y-%m-%d_%H-%M-%S')


def get_current_time():
    """
    Returns current time for logging
    """
    local_tz = pytz.timezone(LOCAL_TIMEZONE)
    return datetime.now(local_tz).isoformat()


def timed_path(base_path, filename: str, timestamp):
    """
    joint path with time stamp
    """
    return os.path.join(base_path, f"{filename}_{timestamp}.jsonl")
