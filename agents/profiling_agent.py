import pandas as pd


class ProfilingAgent:

    def analyze(self, df):
        """
        Performs dataset profiling and returns metadata about the dataset.

        Parameters:
            df (pandas.DataFrame)

        Returns:
            dict containing dataset profile
        """

        profile = {}

        # Dataset shape
        profile["rows"], profile["columns"] = df.shape

        # Column names
        profile["column_names"] = list(df.columns)

        # Data types
        profile["data_types"] = df.dtypes.astype(str).to_dict()

        # Missing values
        profile["missing_values"] = df.isnull().sum().to_dict()

        # Duplicate rows
        profile["duplicate_rows"] = int(df.duplicated().sum())

        # Basic statistics (numeric columns)
        profile["statistics"] = df.describe().to_dict()

        return profile