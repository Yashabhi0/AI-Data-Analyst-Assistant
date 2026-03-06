class OutlierDetectionAgent:

    def detect(self, df):
        """
        Detects outliers in numeric columns using the IQR method.

        Parameters:
            df (pandas.DataFrame)

        Returns:
            dict containing outliers per column
        """

        outliers = {}

        numeric_cols = df.select_dtypes(include=['number']).columns

        for col in numeric_cols:

            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1

            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            column_outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]

            outliers[col] = {
                "count": len(column_outliers),
                "indices": column_outliers.index.tolist()
            }

        return outliers