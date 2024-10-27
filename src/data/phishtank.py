"""
Load the PhishTank database.
https://phishtank.org/developer_info.php
"""

import os
import gzip
import pandas as pd
import requests
from io import BytesIO

from src.data.models import SessionLocal, Source, engine

PHISHTANK_DATASET_URL = "http://data.phishtank.com/data/online-valid.csv.gz"
LOCAL_FILE_PATH = "downloads/phishtank.csv.gz"


def download_file(url, path):
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful
    with open(path, 'wb') as f:
        f.write(response.content)


def load_dataset(path):
    # Check if the file exists locally
    if not os.path.isfile(path):
        download_file(PHISHTANK_DATASET_URL, path)

    # Decompress the .gz file
    with gzip.open(path, 'rb') as f:
        csv_content = f.read()

    # Load the CSV content into a pandas DataFrame
    return pd.read_csv(BytesIO(csv_content))


if __name__ == "__main__":
    dataset = load_dataset(LOCAL_FILE_PATH)
    s = SessionLocal()

    try:
        # Create a new source
        source = Source(name="PhishTank", url=PHISHTANK_DATASET_URL)
        s.add(source)
        s.commit()

        # Create a new DataFrame
        df = dataset[['url']].copy()
        df['source_id'] = source.id
        df['is_phishing'] = True
        df['is_online'] = False

        # Insert the DataFrame into the SQL database
        df.to_sql('url', con=s.bind, if_exists='append', index=False)
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()
