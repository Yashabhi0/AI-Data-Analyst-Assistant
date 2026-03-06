import os
from loaders.csv_loader import load_csv
from loaders.excel_loader import load_excel
from loaders.kaggle_loader import load_kaggle_dataset


class DataLoaderAgent:

    def load(self, source):
        """
        Determines the dataset type and loads it accordingly.
        
        Parameters:
            source (str): file path OR Kaggle dataset name
            
        Returns:
            pandas.DataFrame
        """

        # Check if source is a local file
        if os.path.isfile(source):

            if source.endswith(".csv"):
                print("Loading CSV dataset...")
                return load_csv(source)

            elif source.endswith(".xlsx") or source.endswith(".xls"):
                print("Loading Excel dataset...")
                return load_excel(source)

            else:
                raise ValueError("Unsupported file format")

        # Otherwise assume Kaggle dataset
        else:
            print("Fetching dataset from Kaggle...")
            return load_kaggle_dataset(source)