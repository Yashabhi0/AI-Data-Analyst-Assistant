import pandas as pd


class DataCleaningAgent:

    def handle_missing_values(self, df):

        missing_summary = df.isnull().sum()

        for column in df.columns:

            if df[column].isnull().sum() > 0:

                if pd.api.types.is_numeric_dtype(df[column]):

                    median_value = df[column].median()
                    df[column].fillna(median_value, inplace=True)

                else:

                    mode_value = df[column].mode()[0]
                    df[column].fillna(mode_value, inplace=True)

        return df, missing_summary