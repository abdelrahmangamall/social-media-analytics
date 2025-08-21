import sys
import os
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.pipeline.main import main

def parse_arguments():
    parser = argparse.ArgumentParser(description='Run Social Media Analytics Pipeline')
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug mode with detailed logging')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    main()