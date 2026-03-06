import pandas as pd

def load_excel(file_path):
    """
    Loads an Excel file into a pandas DataFrame.

    Parameters:
        file_path (str): Path to the Excel file

    Returns:
        pandas.DataFrame or None
    """
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return None