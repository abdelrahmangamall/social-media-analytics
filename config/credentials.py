import os
from dotenv import load_dotenv
import logging

load_dotenv()

class Credentials:
    TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
    TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
    TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")

    @classmethod
    def validate(cls):
        logger = logging.getLogger("credentials_validator")
        if not cls.YOUTUBE_API_KEY or 'your_' in cls.YOUTUBE_API_KEY:
            logger.error("YouTube API key is required")
            return False
        if not cls.FACEBOOK_ACCESS_TOKEN or 'your_' in cls.FACEBOOK_ACCESS_TOKEN:
            logger.warning("Facebook access token not configured")
        logger.info("Credentials validation passed")
        return True