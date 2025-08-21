import os
from dotenv import load_dotenv
import logging

def check_environment_variables():
    load_dotenv()
    required_vars = {
        'TWITTER_API_KEY': 'Twitter API Key',
        'TWITTER_API_SECRET': 'Twitter API Secret',
        'TWITTER_ACCESS_TOKEN': 'Twitter Access Token',
        'TWITTER_ACCESS_SECRET': 'Twitter Access Secret',
        'YOUTUBE_API_KEY': 'YouTube API Key'
    }
    logger = logging.getLogger("config_checker")
    missing_vars = []
    empty_vars = []
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value is None:
            missing_vars.append(var)
        elif value.strip() == '' or 'your_' in value:
            empty_vars.append(f"{var} ({description})")
    if missing_vars:
        logger.error(f"Missing environment variables: {', '.join(missing_vars)}")
        return False
    if empty_vars:
        logger.error(f"Empty or placeholder values found: {', '.join(empty_vars)}")
        logger.error("Please update your .env file with actual API credentials")
        return False
    logger.info("All environment variables are properly set")
    return True