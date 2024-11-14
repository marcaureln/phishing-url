import os
import pickle
import requests


def download_file(url, path):
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful
    with open(path, 'wb') as f:
        f.write(response.content)

def cache_dataset(path: str, load_dataset: callable, *args, **kwargs):
    """
    Loads a dataset from a file if it exists, otherwise it loads it from the source and saves it to the file.
    """
    if os.path.isfile(path):
        with open(path, "rb") as f:
            data = pickle.load(f)
        return data

    # Load the dataset from the source
    data = load_dataset(*args, **kwargs)
    with open(path, "wb") as f:
        pickle.dump(data, f)
    return data