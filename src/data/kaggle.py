"""
Load Kaggle Malicious URLs dataset
https://www.kaggle.com/datasets/sid321axn/malicious-urls-dataset/data
"""

import os

import kagglehub
import pandas as pd

from src.data.models import SessionLocal, Source


def load_dataset():
    # Make sure to have your credentials under ~/.kaggle/kaggle.json
    path = kagglehub.dataset_download("sid321axn/malicious-urls-dataset")
    filename = os.path.join(path, "malicious_phish.csv")

    return pd.read_csv(filename)


if __name__ == "__main__":
    dataset = load_dataset()
    s = SessionLocal()

    try:
        # Create a new source
        source = Source(
            name="Kaggle Malicious URLs",
            url="https://www.kaggle.com/datasets/sid321axn/malicious-urls-dataset/data"
        )
        s.add(source)
        s.commit()

        # Create a new DataFrame
        df = dataset[['url', 'type']].copy()
        df.rename(columns={'type': 'is_phishing'}, inplace=True)
        # Filter the dataset to only include phishing and benign (legitimate) URLs
        df = df[df['is_phishing'].isin(['phishing', 'benign'])]
        # Convert the label column to a boolean, in the Kaggle dataset, phishing is labeled as 'phishing'
        df['is_phishing'] = df['is_phishing'].apply(lambda x: x == 'phishing')
        df['source_id'] = source.id
        df['is_online'] = False

        # Insert the DataFrame into the SQL database
        df.to_sql('url', con=s.bind, if_exists='append', index=False)
    except Exception as e:
        s.rollback()
        print(e)
    finally:
        s.close()
