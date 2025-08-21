import googleapiclient.discovery
import pandas as pd
from typing import Dict, Any, List
from .base_client import BaseAPIClient
from config.credentials import Credentials
from config.api_config import APIConfig
import logging
from datetime import datetime
import dateutil.parser

class YouTubeClient(BaseAPIClient):
    def __init__(self):
        super().__init__("youtube")
        self.logger = logging.getLogger("youtube_client")
        try:
            self.youtube = googleapiclient.discovery.build(
                "youtube", "v3", developerKey=Credentials.YOUTUBE_API_KEY
            )
            self.config = APIConfig.load_config().youtube
            self.logger.info("YouTube client initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize YouTube client: {e}")
            raise

    def _make_request(self) -> Dict[str, Any]:
        try:
            search_request = self.youtube.search().list(
                q=self.config['search_query'],
                part="id",
                maxResults=self.config['max_results'],
                type="video",
                order="date"
            )
            search_response = search_request.execute()
            video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
            if not video_ids:
                return {}
            videos_request = self.youtube.videos().list(
                part="snippet,statistics",
                id=",".join(video_ids)
            )
            return videos_request.execute()
        except Exception as e:
            self.logger.error(f"YouTube API error: {e}")
            return {}

    def _transform_response(self, raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        transformed = []
        if 'items' not in raw_data or not raw_data['items']:
            self.logger.warning("No videos found in YouTube response")
            return transformed
        for item in raw_data.get('items', []):
            try:
                stats = item.get('statistics', {})
                snippet = item.get('snippet', {})
                published_at = snippet.get('publishedAt', '')
                if published_at:
                    dt = dateutil.parser.parse(published_at)
                    published_at_naive = dt.replace(tzinfo=None)
                else:
                    published_at_naive = None
                transformed.append({
                    'post_id': item['id'],
                    'content': snippet.get('title', ''),
                    'likes': int(stats.get('likeCount', 0)),
                    'comments': int(stats.get('commentCount', 0)),
                    'shares': 0,
                    'post_date': published_at_naive,
                    'author_id': snippet.get('channelId', ''),
                    'author_name': snippet.get('channelTitle', '')
                })
            except Exception as e:
                self.logger.warning(f"Failed to transform video: {e}")
                continue
        self.logger.info(f"Transformed {len(transformed)} YouTube videos")
        return transformed