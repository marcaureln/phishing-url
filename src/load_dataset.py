from sqlalchemy.orm import Session
from ucimlrepo import fetch_ucirepo
from database import SessionLocal, Source
from utils import cache_dataset, download_file
import pandas as pd
import kagglehub
import os
import gzip
from io import BytesIO


def load_phiusiil():
    """
    Load the PhiUSIIL Phishing URL dataset.
    https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset
    """
    phiusiil_dataset_id = 967
    dataset_path = f"downloads/id_{phiusiil_dataset_id}.pkl"
    dataset = cache_dataset(dataset_path, fetch_ucirepo, id=phiusiil_dataset_id)

    metadata = {'name': "PhiUSIIL Phishing URL", 'url': dataset.metadata.repository_url}

    df = dataset.data.original[['URL', 'label']].copy()
    # Rename the columns to match the URL table
    df.rename(columns={'URL': 'url', 'label': 'is_phishing'}, inplace=True)
    # Convert the label column to a boolean, 0 is phishing and 1 is legitimate.
    df['is_phishing'] = df['is_phishing'].apply(lambda x: x == 0)

    return metadata, df


def load_kaggle_malicious_phish():
    """
    Load Kaggle Malicious URLs dataset
    https://www.kaggle.com/datasets/sid321axn/malicious-urls-dataset/data
    """
    # Make sure to have your credentials under ~/.kaggle/kaggle.json
    path = kagglehub.dataset_download("sid321axn/malicious-urls-dataset")
    filename = os.path.join(path, "malicious_phish.csv")

    metadata = {'name': "Kaggle Malicious URLs",
                'url': "https://www.kaggle.com/datasets/sid321axn/malicious-urls-dataset/data"}

    df = pd.read_csv(filename)
    # Keep only the URL and type columns and rename type to is_phishing
    df = df[['url', 'type']]
    df.rename(columns={'type': 'is_phishing'}, inplace=True)
    # Filter the dataset to only include phishing and benign (legitimate) URLs
    df = df[df['is_phishing'].isin(['phishing', 'benign'])]
    # Convert the label column to a boolean, in the Kaggle dataset, phishing is labeled as 'phishing'
    df['is_phishing'] = df['is_phishing'].apply(lambda x: x == 'phishing')

    return metadata, df


def load_phishtank():
    """
    Load the PhishTank database.
    https://phishtank.org/developer_info.php
    """
    phishtank_dataset_url = "http://data.phishtank.com/data/online-valid.csv.gz"
    phishtank_dataset_path = "downloads/phishtank.csv.gz"

    # Check if the file exists locally
    if not os.path.isfile(phishtank_dataset_path):
        download_file(phishtank_dataset_url, phishtank_dataset_path)

    # Decompress the .gz file
    with gzip.open(phishtank_dataset_path, 'rb') as f:
        csv_content = f.read()

    metadata = {'name': "PhishTank", 'url': phishtank_dataset_url}

    # Load the CSV content into a pandas DataFrame
    df = pd.read_csv(BytesIO(csv_content))
    df = df[['url']]
    # This dataset only contains phishing URLs
    df['is_phishing'] = True

    return metadata, df


def load_dataset(session: Session, metadata: dict, df: pd.DataFrame):
    # Create a new source
    source = Source(**metadata)
    session.add(source)
    # Commit the transaction to get the source ID
    session.commit()

    # Add the source ID to the DataFrame
    df['source_id'] = source.id
    # We assume that all the websites are not online anymore
    df['is_online'] = False

    # Insert the new DataFrame into the SQL database
    df.to_sql(
        name="url",  # Table name
        con=session.bind,  # Database connection
        if_exists="append",  # Do not replace nor drop the table
        index=False  # Do not include the DataFrame index
    )


if __name__ == "__main__":
    s = SessionLocal()

    try:
        load_dataset(s, *load_phiusiil())
        load_dataset(s, *load_kaggle_malicious_phish())
        load_dataset(s, *load_phishtank())
    except Exception as e:
        print(e)
        s.rollback()
    finally:
        s.close()
