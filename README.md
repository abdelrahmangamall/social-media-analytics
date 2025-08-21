# Social Media Analytics Pipeline

A robust data engineering pipeline that collects, processes, and analyzes social media data from multiple platforms. The system computes engagement metrics, identifies top-performing content, and generates comprehensive analytics reports.

---

## 📋 Features
- **Multi-Platform Data Collection:** Supports YouTube, Facebook, and Twitter APIs  
- **Data Normalization:** Unified schema across all social media platforms  
- **Advanced Analytics:** Daily engagement metrics, top posts identification, moving averages  
- **Error Handling:** Robust error handling and fallback mechanisms  
- **Automation:** Ready for daily execution and Airflow scheduling  
- **Multiple Output Formats:** CSV and Parquet file support  


---
## 🏗️ Project Structure
```bash

social-media-analytics/
├── config/
│   ├── api_config.py
│   └── credentials.py
├── src/
│   ├── api/
│   │   ├── base_client.py
│   │   ├── youtube_client.py
│   │   ├── facebook_client.py
│   │   └── twitter_client.py
│   ├── core/
│   │   ├── data_processor.py
│   │   ├── analyzer.py
│   │   ├── utils.py
│   │   └── config_checker.py
│   └── pipeline/
│       ├── main.py
│       ├── results.py
│       └── airflow_dag.py
├── scripts/
│   └── run_pipeline.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── analytics/
├── requirements.txt
└── README.md
```
---

## 🚀 Quick Start


### Run the pipeline
```bash
# Method 1: Using the script
python scripts/run_pipeline.py

# Method 2: Directly from main
python -m src.pipeline.main

# Method 3: View results
python -m src.pipeline.results
```
---
### Prerequisites
- Python 3.8+  
- YouTube API key  
- Twitter API credentials *(optional)*  
- Facebook access token *(optional)*  

### Installation
Clone the repository:
```bash
git clone <repository-url>
cd social-media-analytics

Install dependencies:

pip install -r requirements.txt


Configure API credentials by creating a .env file:

YOUTUBE_API_KEY=your_youtube_api_key_here
TWITTER_API_KEY=your_twitter_api_key_here
TWITTER_API_SECRET=your_twitter_api_secret_here
TWITTER_ACCESS_TOKEN=your_twitter_access_token_here
TWITTER_ACCESS_SECRET=your_twitter_access_secret_here
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token_here

Usage

Run the pipeline:

python scripts/run_pipeline.py


Or directly:

python -m src.pipeline.main


View results:

python -m src.pipeline.results

📊 Output Files

data/raw/real_data_*.parquet → Raw collected data

data/processed/processed_real_data_*.parquet → Normalized data

data/analytics/real_daily_metrics_*.csv → Daily engagement metrics

data/analytics/real_top_posts_overall_*.csv → Top 5 posts overall

data/analytics/real_top_posts_platform_*.csv → Top 3 posts per platform

🔧 API Support

✅ YouTube API – Fully functional, requires API key

✅ Facebook API – Mock data (real API requires access token)

⚠️ Twitter API – Limited (requires paid access), uses fallback

📈 Analytics Features

Daily Metrics: Engagement score sum/mean/count, likes/comments/shares totals, 7-day moving average

Top Posts: Top 5 overall + top 3 per platform by engagement

Data Processing: Schema normalization, missing value handling, timestamp standardization, engagement score calculation

🛠️ Configuration

Modify config/api_config.py for:

Search queries and parameters

Rate limits and request limits

Platform-specific settings

🔄 Automation

Airflow Integration: Use the provided DAG for scheduled execution

Manual Scheduling: Add to crontab for daily execution:

0 0 * * * cd /path/to/social-media-analytics && python scripts/run_pipeline.py

🐛 Troubleshooting

Common Issues:

YouTube API errors → Verify API key and enable YouTube Data API v3

SSL errors → Update certificates with pip install --upgrade certifi

Import errors → Set Python path:

export PYTHONPATH=/path/to/project


Data not collected → Check API quotas and network connectivity

Debug Mode:

python scripts/run_pipeline.py --debug

📝 License

Educational use only. Ensure compliance with API terms of service.

🤝 Contributing

Fork repository

Create feature branch

Make changes and test

Submit pull request
