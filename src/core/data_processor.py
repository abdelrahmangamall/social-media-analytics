import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Any, List

class DataProcessor:
    SCHEMA = {
        'platform': 'object',
        'post_id': 'object',
        'content': 'object',
        'likes': 'int64',
        'comments': 'int64',
        'shares': 'int64',
        'post_date': 'datetime64[ns]',
        'author_id': 'object',
        'engagement_score': 'int64',
        'collected_at': 'datetime64[ns]'
    }

    @staticmethod
    def normalize_data(df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
        for col in DataProcessor.SCHEMA.keys():
            if col not in df.columns and col != 'engagement_score':
                df[col] = np.nan
        numeric_cols = ['likes', 'comments', 'shares']
        df[numeric_cols] = df[numeric_cols].fillna(0)
        df['content'] = df['content'].fillna('')
        if 'post_date' in df.columns:
            df['post_date'] = pd.to_datetime(df['post_date'], errors='coerce', utc=True).dt.tz_convert(None)
        if 'collected_at' in df.columns:
            df['collected_at'] = pd.to_datetime(df['collected_at'], errors='coerce', utc=True).dt.tz_convert(None)
        for col, dtype in DataProcessor.SCHEMA.items():
            if col in df.columns and col not in ['post_date', 'collected_at']:
                try:
                    df[col] = df[col].astype(dtype)
                except Exception as e:
                    print(f"Warning: Could not convert {col} to {dtype}: {e}")
        df['engagement_score'] = df['likes'] + df['comments'] + df['shares']
        return df

    @staticmethod
    def validate_data(df: pd.DataFrame) -> bool:
        if df.empty:
            return True
        required_cols = list(DataProcessor.SCHEMA.keys())
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        return True