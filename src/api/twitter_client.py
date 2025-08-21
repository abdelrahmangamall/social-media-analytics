import tweepy
import pandas as pd
from typing import Dict, Any, List
from .base_client import BaseAPIClient
from config.credentials import Credentials
import logging
import os
from dotenv import load_dotenv
import snscrape.modules.twitter as sntwitter

class TwitterClient(BaseAPIClient):
    def __init__(self):
        super().__init__("twitter")
        self.logger = logging.getLogger("twitter_client")
        load_dotenv()
        try:
            self.auth = tweepy.OAuthHandler(
                os.getenv('TWITTER_API_KEY'),
                os.getenv('TWITTER_API_SECRET')
            )
            self.auth.set_access_token(
                os.getenv('TWITTER_ACCESS_TOKEN'),
                os.getenv('TWITTER_ACCESS_SECRET')
            )
            self.api = tweepy.API(self.auth, wait_on_rate_limit=True)
            self.use_tweepy = True
            self.logger.info("Twitter client initialized with Tweepy")
        except Exception as e:
            self.logger.warning(f"Tweepy init failed: {e}")
            self.use_tweepy = False

    def _make_request(self, query: str = "#datascience OR #machinelearning", count: int = 100) -> List[Any]:
        if self.use_tweepy:
            try:
                tweets = self.api.search_tweets(q=query, count=count, tweet_mode='extended')
                self.logger.info(f"Fetched {len(tweets)} tweets")
                return tweets
            except Exception as e:
                self.logger.warning(f"Tweepy request failed: {e}")
                self.use_tweepy = False
        tweets = []
        try:
            for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
                if i >= count:
                    break
                tweets.append(tweet)
            self.logger.info(f"Fetched {len(tweets)} tweets")
        except Exception as e:
            self.logger.error(f"snscrape failed: {e}")
        return tweets

    def _transform_response(self, tweets: List[Any]) -> List[Dict[str, Any]]:
        transformed = []
        if not tweets:
            return transformed
        if self.use_tweepy and isinstance(tweets[0], tweepy.Tweet):
            for tweet in tweets:
                transformed.append({
                    'post_id': tweet.id_str,
                    'content': tweet.full_text,
                    'likes': tweet.favorite_count,
                    'comments': 0,
                    'shares': tweet.retweet_count,
                    'post_date': tweet.created_at,
                    'author_id': tweet.user.id_str,
                    'author_name': tweet.user.screen_name
                })
        else:
            for tweet in tweets:
                transformed.append({
                    'post_id': str(tweet.id),
                    'content': tweet.content,
                    'likes': 0,
                    'comments': 0,
                    'shares': 0,
                    'post_date': tweet.date,
                    'author_id': tweet.user.username,
                    'author_name': tweet.user.displayname
                })
        return transformed