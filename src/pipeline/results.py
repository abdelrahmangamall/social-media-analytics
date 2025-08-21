import pandas as pd
import os
import glob
from datetime import datetime

def find_latest_file(pattern):
    files = glob.glob(pattern)
    if not files:
        return None
    return max(files, key=os.path.getctime)

def display_results():
    try:
        daily_metrics_file = find_latest_file('data/analytics/daily_metrics_*.csv')
        top_posts_file = find_latest_file('data/analytics/top_posts_overall_*.csv')
        top_platform_file = find_latest_file('data/analytics/top_posts_platform_*.csv')
        if not daily_metrics_file:
            print("No analytics files found. Run the pipeline first.")
            return
        print(f"Loading results from: {daily_metrics_file}")
        daily_metrics = pd.read_csv(daily_metrics_file)
        print("Daily Metrics:")
        print(daily_metrics.head(10))
        if top_posts_file:
            top_posts = pd.read_csv(top_posts_file)
            print("Top Posts Overall:")
            print(top_posts.head())
        if top_platform_file:
            top_platform = pd.read_csv(top_platform_file)
            print("Top Posts Per Platform:")
            print(top_platform.head(12))
        print("Summary:")
        print(f"Total records processed: {len(daily_metrics.groupby('date').sum())} days")
        print(f"Platforms: {', '.join(daily_metrics['platform'].unique())}")
    except Exception as e:
        print(f"Error loading results: {e}")

if __name__ == "__main__":
    display_results()