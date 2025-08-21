import sys
import os
import pandas as pd
import logging
from datetime import datetime
from typing import Dict, Any

current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.abspath(os.path.join(current_dir, '..', '..'))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

try:
    from src.api.twitter_client import TwitterClient
    from src.api.youtube_client import YouTubeClient
    from src.core.data_processor import DataProcessor
    from src.core.analyzer import AnalyticsEngine
    from src.core.utils import setup_logging, save_data
except ImportError as e:
    print(f"Import error: {e}")
    print("Current sys.path:", sys.path)
    raise

class SocialMediaPipeline:
    def __init__(self):
        self.logger = setup_logging("pipeline")
        self.clients = {}
        try:
            from src.api.youtube_client import YouTubeClient
            self.clients['youtube'] = YouTubeClient()
            self.logger.info("YouTube client loaded successfully")
        except Exception as e:
            self.logger.error(f"YouTube client not available: {e}")
            raise
        try:
            from src.api.facebook_client import FacebookClient
            self.clients['facebook'] = FacebookClient()
            self.logger.info("Facebook client loaded successfully")
        except Exception as e:
            self.logger.warning(f"Facebook client not available: {e}")
        try:
            from src.api.twitter_client import TwitterClient
            self.clients['twitter'] = TwitterClient()
            self.logger.info("Twitter client loaded successfully")
        except Exception as e:
            self.logger.warning(f"Twitter client not available: {e}")
        if not self.clients:
            self.logger.error("No API clients available")
            raise ValueError("No API clients available")
        self.processor = DataProcessor()
        self.analyzer = AnalyticsEngine()

    def collect_data(self) -> pd.DataFrame:
        return self._collect_real_data()

    def _collect_real_data(self) -> pd.DataFrame:
        all_data = []
        for platform, client in self.clients.items():
            try:
                self.logger.info(f"Collecting data from {platform}...")
                platform_data = client.fetch_data()
                if not platform_data.empty:
                    all_data.append(platform_data)
                    self.logger.info(f"Collected {len(platform_data)} records from {platform}")
                else:
                    self.logger.warning(f"No data collected from {platform}")
            except Exception as e:
                self.logger.error(f"Error collecting data from {platform}: {str(e)}")
                continue
        if all_data:
            return pd.concat(all_data, ignore_index=True)
        else:
            self.logger.error("No data collected from any platform")
            return pd.DataFrame()

    def process_data(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        if raw_data.empty:
            return raw_data
        try:
            processed_data = self.processor.normalize_data(raw_data)
            self.processor.validate_data(processed_data)
            self.logger.info(f"Processed {len(processed_data)} records")
            return processed_data
        except Exception as e:
            self.logger.error(f"Error processing data: {str(e)}")
            raise

    def analyze_data(self, processed_data: pd.DataFrame) -> Dict[str, Any]:
        try:
            daily_metrics = self.analyzer.compute_daily_metrics(processed_data)
            daily_metrics = self.analyzer.compute_moving_average(daily_metrics)
            top_posts = self.analyzer.identify_top_posts(processed_data)
            self.logger.info("Analytics completed successfully")
            return {
                'daily_metrics': daily_metrics,
                'top_posts': top_posts
            }
        except Exception as e:
            self.logger.error(f"Error during analytics: {str(e)}")
            raise

    def run(self):
        self.logger.info("Starting social media analytics pipeline with REAL APIs")
        try:
            raw_data = self.collect_data()
            if raw_data.empty:
                self.logger.warning("No data collected from any platform")
                return
            processed_data = self.process_data(raw_data)
            analytics_results = self.analyze_data(processed_data)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_data(raw_data, f"data/raw/real_data_{timestamp}.parquet")
            save_data(processed_data, f"data/processed/processed_real_data_{timestamp}.parquet")
            save_data(analytics_results['daily_metrics'], f"data/analytics/real_daily_metrics_{timestamp}.csv")
            save_data(analytics_results['top_posts']['top_overall'],
                      f"data/analytics/real_top_posts_overall_{timestamp}.csv")
            save_data(analytics_results['top_posts']['top_per_platform'],
                      f"data/analytics/real_top_posts_platform_{timestamp}.csv")
            self.logger.info(f"Pipeline completed successfully. Processed {len(processed_data)} REAL records")
        except Exception as e:
            self.logger.error(f"Pipeline failed: {str(e)}")
            raise

def main():
    from config.credentials import Credentials
    from src.core.config_checker import check_environment_variables
    if not check_environment_variables():
        print("Please fix your .env file before running the pipeline")
        return
    if not Credentials.validate():
        print("Invalid credentials. Please check your .env file")
        return
    pipeline = SocialMediaPipeline()
    pipeline.run()

if __name__ == "__main__":
    main()