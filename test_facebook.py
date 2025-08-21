# test_facebook_fixed.py
import os
from dotenv import load_dotenv
from src.api.facebook_client import FacebookClient
import pandas as pd

load_dotenv()


def test_facebook_client():
    """اختبار Facebook Client الجديد"""
    print("Testing updated Facebook client...")

    try:
        client = FacebookClient()

        if client.use_mock_data:
            print("✅ Using mock data (API access restricted)")
        else:
            print("✅ Using real API data")

        # اختبار جلب البيانات
        data = client.fetch_data()

        if not data.empty:
            print(f"✅ Success! Collected {len(data)} Facebook posts")
            print(f"📊 Sample data:")
            print(data[['post_id', 'content', 'likes', 'comments']].head(2))
            return True
        else:
            print("❌ No data collected")
            return False

    except Exception as e:
        print(f"❌ Error testing Facebook client: {e}")
        return False


if __name__ == "__main__":
    test_facebook_client()