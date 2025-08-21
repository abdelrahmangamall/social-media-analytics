import pandas as pd
from typing import Dict, Any, List
from .base_client import BaseAPIClient
from config.credentials import Credentials
from config.api_config import APIConfig
import logging
from datetime import datetime, timedelta
import random

class FacebookClient(BaseAPIClient):
    def __init__(self):
        super().__init__("facebook")
        self.logger = logging.getLogger("facebook_client")
        self.access_token = Credentials.FACEBOOK_ACCESS_TOKEN
        self.use_mock_data = not self._validate_token()
        if self.use_mock_data:
            self.logger.warning("Using mock data for Facebook")
        else:
            self.logger.info("Facebook client initialized with real API")

    def _validate_token(self):
        if not self.access_token or self.access_token == 'your_facebook_access_token_here':
            return False
        return True

    def _make_request(self, page_id: str) -> Dict[str, Any]:
        if self.use_mock_data:
            return self._generate_mock_data(page_id)
        else:
            return {}

    def _generate_mock_data(self, page_id: str) -> Dict[str, Any]:
        try:
            mock_posts = []
            base_date = datetime.now() - timedelta(days=30)
            for i in range(15):
                post_date = base_date + timedelta(days=random.randint(0, 30))
                content_options = [
                    "Exciting news from our team! Stay tuned for updates.",
                    "Check out our latest product release!",
                    "We're happy to announce our new partnership!",
                    "Behind the scenes: how we create amazing content!",
                    "Thank you to all our amazing followers!",
                    "Breaking news in the tech world!",
                    "Our team is growing! Welcome to our new members!",
                    "Special offer just for our Facebook followers!",
                    "Behind the scenes of our latest project!",
                    "We've reached an amazing milestone!"
                ]
                content = random.choice(content_options)
                mock_posts.append({
                    'id': f"{page_id}_{i}",
                    'message': content,
                    'created_time': post_date.isoformat() + 'Z',
                    'likes': {'summary': {'total_count': random.randint(50, 2000)}},
                    'comments': {'summary': {'total_count': random.randint(5, 300)}},
                    'shares': {'count': random.randint(0, 150)}
                })
            return {'data': mock_posts}
        except Exception as e:
            self.logger.error(f"Error generating mock data: {e}")
            return {}

    def _transform_response(self, raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        transformed = []
        if not raw_data or 'data' not in raw_data:
            return transformed
        for post in raw_data.get('data', []):
            try:
                likes_count = post.get('likes', {}).get('summary', {}).get('total_count', 0)
                comments_count = post.get('comments', {}).get('summary', {}).get('total_count', 0)
                shares_count = post.get('shares', {}).get('count', 0) if post.get('shares') else 0
                created_time = post.get('created_time', '')
                if created_time:
                    dt = datetime.fromisoformat(created_time.replace('Z', '+00:00'))
                    created_time_naive = dt.replace(tzinfo=None)
                else:
                    created_time_naive = None
                transformed.append({
                    'post_id': post['id'],
                    'content': post.get('message', ''),
                    'likes': likes_count,
                    'comments': comments_count,
                    'shares': shares_count,
                    'post_date': created_time_naive,
                    'author_id': post['id'].split('_')[0] if '_' in post['id'] else post['id'],
                    'author_name': f"page_{post['id'].split('_')[0]}" if '_' in post['id'] else "unknown"
                })
            except Exception as e:
                self.logger.warning(f"Failed to transform Facebook post: {e}")
                continue
        return transformed

    def fetch_data(self) -> pd.DataFrame:
        all_data = []
        config = APIConfig.load_config().facebook
        for page_id in config['page_ids']:
            try:
                self.logger.info(f"Processing Facebook page: {page_id}")
                raw_data = self._make_request(page_id)
                if raw_data:
                    page_data = self._transform_response(raw_data)
                    if page_data:
                        df = pd.DataFrame(page_data)
                        all_data.append(df)
                        self.logger.info(f"Collected {len(df)} posts from page {page_id}")
            except Exception as e:
                self.logger.error(f"Error processing page {page_id}: {e}")
                continue
        if all_data:
            return pd.concat(all_data, ignore_index=True)
        else:
            self.logger.warning("No data collected from any Facebook page")
            return pd.DataFrame()