# test_twitter_only.py
import logging
from src.api.twitter_client import TwitterClient

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    print("🚀 Testing Twitter client...")
    try:
        client = TwitterClient()
        tweets = client._make_request(query="#datascience", count=20)
        transformed = client._transform_response(tweets)

        print(f"✅ Collected {len(transformed)} tweets")
        if transformed:
            print("📊 First tweet sample:")
            print(transformed[0])
    except Exception as e:
        print(f"❌ Twitter test failed: {e}")
