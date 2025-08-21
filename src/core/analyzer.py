import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

class AnalyticsEngine:
    @staticmethod
    def compute_daily_metrics(df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return pd.DataFrame()
        df = df.copy()
        df['date'] = df['post_date'].dt.date
        metrics = df.groupby(['platform', 'date']).agg({
            'engagement_score': ['sum', 'mean', 'count'],
            'likes': 'sum',
            'comments': 'sum',
            'shares': 'sum'
        }).round(2)
        metrics.columns = ['_'.join(col).strip('_') for col in metrics.columns.values]
        metrics = metrics.reset_index()
        return metrics

    @staticmethod
    def compute_moving_average(metrics_df: pd.DataFrame, window: int = 7) -> pd.DataFrame:
        if metrics_df.empty:
            return pd.DataFrame()
        metrics_df = metrics_df.sort_values(['platform', 'date'])
        metrics_df['engagement_ma'] = metrics_df.groupby('platform')['engagement_score_sum'] \
            .transform(lambda x: x.rolling(window=window, min_periods=1).mean())
        return metrics_df

    @staticmethod
    def identify_top_posts(df: pd.DataFrame, overall_n: int = 5, platform_n: int = 3) -> Dict[str, pd.DataFrame]:
        if df.empty:
            return {}
        top_overall = df.nlargest(overall_n, 'engagement_score')[
            ['platform', 'post_id', 'content', 'engagement_score', 'likes', 'comments', 'shares']
        ]
        top_per_platform = df.groupby('platform', group_keys=False, observed=True).apply(
            lambda x: x.nlargest(platform_n, 'engagement_score')[
                ['post_id', 'content', 'engagement_score', 'likes', 'comments', 'shares']
            ]
        ).reset_index(drop=True)
        return {
            'top_overall': top_overall,
            'top_per_platform': top_per_platform
        }