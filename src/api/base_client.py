from abc import ABC, abstractmethod
import pandas as pd
import logging
from datetime import datetime
from typing import List, Dict, Any
import time

class BaseAPIClient(ABC):
    def __init__(self, platform_name: str):
        self.platform_name = platform_name
        self.logger = logging.getLogger(f"{platform_name}_client")

    @abstractmethod
    def _make_request(self, endpoint: str, params: Dict[str, Any] = None):
        pass

    @abstractmethod
    def _transform_response(self, raw_data: Any) -> List[Dict[str, Any]]:
        pass

    def fetch_data(self, **kwargs) -> pd.DataFrame:
        try:
            self.logger.info(f"Fetching data from {self.platform_name}")
            raw_data = self._make_request(**kwargs)
            transformed_data = self._transform_response(raw_data)
            df = pd.DataFrame(transformed_data)
            if not df.empty:
                df['platform'] = self.platform_name
                df['collected_at'] = datetime.now()
            self.logger.info(f"Successfully fetched {len(df)} records from {self.platform_name}")
            return df
        except Exception as e:
            self.logger.error(f"Error fetching data from {self.platform_name}: {str(e)}")
            return pd.DataFrame()

    def _handle_rate_limit(self, reset_time: int):
        sleep_time = max(reset_time - time.time(), 0) + 1
        self.logger.warning(f"Rate limit exceeded. Sleeping for {sleep_time:.2f} seconds")
        time.sleep(sleep_time)