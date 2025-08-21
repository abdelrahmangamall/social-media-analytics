from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class APIConfig:
    twitter: Dict[str, Any]
    youtube: Dict[str, Any]
    facebook: Dict[str, Any]

    @classmethod
    def load_config(cls):
        return cls(
            twitter={
                "search_query": "#datascience OR #machinelearning OR #ai",
                "count": 100,
                "rate_limit": 450
            },
            youtube={
                "search_query": "data science OR machine learning",
                "max_results": 50,
                "part": "snippet,statistics"
            },
            facebook={
                "page_ids": [
                    "company_page_1",
                    "company_page_2",
                    "company_page_3",
                    "company_page_4",
                    "company_page_5"
                ],
                "limit": 15,
                "fields": "id,message,created_time,likes.summary(true),comments.summary(true),shares"
            }
        )