"""
Load the PhiUSIIL Phishing URL dataset.
https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset
"""

import os
import pickle

from ucimlrepo import fetch_ucirepo

from src.data.models import SessionLocal, Source, engine


def load_dataset(dataset_id, path):
    """
    Loads the PhiUSIIL Phishing URL dataset.
    It fetches the dataset from the UCI repository and stores it in a pickle file for future use.
    """
    if os.path.isfile(path):
        with open(path, "rb") as f:
            data = pickle.load(f)
    else:
        data = fetch_ucirepo(id=dataset_id)
        with open(path, "wb") as f:
            pickle.dump(data, f)
    return data


if __name__ == "__main__":
    PHIUSIIL_DATASET_ID = 967
    dataset_path = f"downloads/id_{PHIUSIIL_DATASET_ID}.pkl"
    dataset = load_dataset(PHIUSIIL_DATASET_ID, dataset_path)

    s = SessionLocal()

    try:
        # Create a new source
        source = Source(name="PhiUSIIL Phishing URL", url=dataset.metadata.repository_url)
        s.add(source)
        # Commit the transaction to get the source ID
        s.commit()

        # Create a new DataFrame with the specified columns
        df = dataset.data.original[['URL', 'label']].copy()
        # Rename the columns to match the URL table
        df.rename(columns={'URL': 'url', 'label': 'is_phishing'}, inplace=True)
        # Convert the label column to a boolean, in the PhiUSIIL dataset, 0 is phishing and 1 is legitimate.
        df['is_phishing'] = df['is_phishing'].apply(lambda x: x == 0)
        df['source_id'] = source.id
        df['is_online'] = False

        # Insert the new DataFrame into the SQL database
        df.to_sql(
            name="url",  # Table name
            con=engine,  # Database connection
            if_exists="append",  # Do not replace nor drop the table
            index=False  # Do not include the DataFrame index
        )
    except Exception as e:
        s.rollback()
        print(e)
    finally:
        s.close()
