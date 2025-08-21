# test_youtube_only.py
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime

load_dotenv()


def test_youtube_pipeline():
    """اختبار YouTube API في البايبلاين"""
    print("Testing YouTube-only pipeline...")

    try:
        # اختبار YouTube client مباشرة
        from src.api.youtube_client import YouTubeClient
        from src.core.data_processor import DataProcessor

        youtube_client = YouTubeClient()
        data = youtube_client.fetch_data()

        print(f"✅ YouTube data fetched: {len(data)} records")

        if not data.empty:
            # اختبار المعالجة
            processor = DataProcessor()
            processed_data = processor.normalize_data(data)

            print(f"✅ Data processed successfully: {len(processed_data)} records")
            print(f"📊 Columns: {list(processed_data.columns)}")
            print(f"📅 Date range: {processed_data['post_date'].min()} to {processed_data['post_date'].max()}")

            return True
        else:
            print("❌ No data from YouTube")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_youtube_pipeline()