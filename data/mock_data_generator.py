# src/data/mock_data_generator.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import logging
from typing import List, Dict, Any


class MockDataGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def generate_mock_social_media_data(self, num_records: int = 1000) -> pd.DataFrame:
        """
        إنشاء بيانات تجريبية لمشروع تحليل وسائل التواصل الاجتماعي

        Args:
            num_records (int): عدد التسجيلات المطلوبة

        Returns:
            pd.DataFrame: بيانات تجريبية في DataFrame
        """
        platforms = ['twitter', 'facebook', 'youtube', 'instagram']
        authors = [f'user_{i}' for i in range(1, 101)]
        hashtags = ['DataScience', 'AI', 'MachineLearning', 'BigData', 'DataEngineering', 'Python', 'SQL']

        posts = []
        base_date = datetime.now() - timedelta(days=30)

        for i in range(num_records):
            platform = random.choice(platforms)
            post_date = base_date + timedelta(days=random.randint(0, 30),
                                              hours=random.randint(0, 23))

            # إنشاء محتوى عشوائي مع هاشتاجات
            content_templates = [
                "Check out this amazing {} tutorial! #{}",
                "Just launched our new {} product. What do you think? #{}",
                "The future of {} analytics is here. #{}",
                "How {} is transforming industries. #{}",
                "5 tips for becoming a better {} engineer. #{}",
                "Latest trends in {} for 2024. #{}"
            ]

            topic = random.choice(['data', 'AI', 'machine learning', 'big data', 'data engineering'])
            hashtag = random.choice(hashtags)
            content_template = random.choice(content_templates)
            content = content_template.format(topic, hashtag)

            # إضافة هاشتاجات إضافية
            additional_hashtags = random.sample(hashtags, random.randint(1, 3))
            for extra_hashtag in additional_hashtags:
                if extra_hashtag != hashtag:
                    content += f" #{extra_hashtag}"

            # إنشاء إحصائيات Engagement بناءً على المنصة
            engagement_stats = self._generate_engagement_stats(platform)

            posts.append({
                'post_id': f'{platform}_{i}_{random.randint(1000, 9999)}',
                'content': content,
                'likes': engagement_stats['likes'],
                'comments': engagement_stats['comments'],
                'shares': engagement_stats['shares'],
                'post_date': post_date,
                'platform': platform,
                'author_id': random.choice(authors),
                'language': random.choice(['en', 'ar', 'es', 'fr']),
                'hashtags': ', '.join([hashtag] + additional_hashtags)
            })

        df = pd.DataFrame(posts)
        self.logger.info(f"تم إنشاء {len(df)} تسجيل تجريبي")
        return df

    def _generate_engagement_stats(self, platform: str) -> Dict[str, int]:
        """إنشاء إحصائيات engagement واقعية بناءً على المنصة"""
        if platform == 'twitter':
            return {
                'likes': random.randint(5, 500),
                'comments': random.randint(0, 100),
                'shares': random.randint(0, 200)
            }
        elif platform == 'facebook':
            return {
                'likes': random.randint(10, 1000),
                'comments': random.randint(0, 200),
                'shares': random.randint(0, 300)
            }
        elif platform == 'youtube':
            return {
                'likes': random.randint(20, 5000),
                'comments': random.randint(0, 500),
                'shares': random.randint(0, 100)
            }
        else:  # instagram
            return {
                'likes': random.randint(50, 2000),
                'comments': random.randint(0, 300),
                'shares': random.randint(0, 150)
            }

    def save_mock_data(self, df: pd.DataFrame, filepath: str):
        """حفظ البيانات التجريبية في ملف"""
        try:
            df.to_csv(filepath, index=False, encoding='utf-8')
            self.logger.info(f"تم حفظ البيانات في {filepath}")
        except Exception as e:
            self.logger.error(f"خطأ في حفظ البيانات: {str(e)}")
            raise


# دالة مساعدة للاستخدام المباشر
def generate_and_save_mock_data(num_records: int = 1000, output_path: str = "data/raw/mock_social_media_data.csv"):
    """إنشاء وحفظ بيانات تجريبية"""
    generator = MockDataGenerator()
    mock_data = generator.generate_mock_social_media_data(num_records)
    generator.save_mock_data(mock_data, output_path)
    return mock_data


if __name__ == "__main__":
    # عند التشغيل المباشر، إنشاء بيانات تجريبية
    generate_and_save_mock_data(1000)