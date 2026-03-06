import os
import zipfile
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi


def load_kaggle_dataset(dataset_name, download_path="datasets"):
    """
    Downloads a Kaggle dataset and loads the first CSV file into a DataFrame.

    Parameters:
        dataset_name (str): Kaggle dataset identifier (e.g., "zynicide/wine-reviews")
        download_path (str): Folder where dataset will be downloaded

    Returns:
        pandas.DataFrame or None
    """

    try:
        # Initialize Kaggle API
        api = KaggleApi()
        api.authenticate()

        # Create download directory if not exists
        os.makedirs(download_path, exist_ok=True)

        # Download dataset
        api.dataset_download_files(dataset_name, path=download_path, unzip=True)

        # Find first CSV file
        for file in os.listdir(download_path):
            if file.endswith(".csv"):
                file_path = os.path.join(download_path, file)
                df = pd.read_csv(file_path)
                return df

        print("No CSV file found in dataset.")
        return None

    except Exception as e:
        print(f"Error loading Kaggle dataset: {e}")
        return None