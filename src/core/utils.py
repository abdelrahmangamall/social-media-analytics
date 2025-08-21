import logging
import pandas as pd
import os
from typing import Union
import sys

def setup_logging(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)
    return logger

def save_data(data: pd.DataFrame, filepath: str):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if filepath.endswith('.parquet'):
        data.to_parquet(filepath, index=False)
    elif filepath.endswith('.csv'):
        data.to_csv(filepath, index=False)
    elif filepath.endswith('.json'):
        data.to_json(filepath, orient='records', indent=2)
    else:
        raise ValueError(f"Unsupported file format: {filepath}")