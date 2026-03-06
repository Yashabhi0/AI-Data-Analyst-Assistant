import pandas as pd


class PatternDetectionAgent:

    def detect(self, df, correlation_threshold=0.7):
        """
        Detects strong correlations and patterns in numeric data.

        Parameters:
            df (pandas.DataFrame)
            correlation_threshold (float): threshold for strong correlation

        Returns:
            dict containing detected patterns
        """

        patterns = {}

        numeric_df = df.select_dtypes(include=["number"])

        if numeric_df.shape[1] < 2:
            patterns["correlations"] = []
            return patterns

        corr_matrix = numeric_df.corr()

        strong_correlations = []

        for col1 in corr_matrix.columns:
            for col2 in corr_matrix.columns:
                if col1 != col2:
                    corr_value = corr_matrix.loc[col1, col2]

                    if abs(corr_value) >= correlation_threshold:
                        strong_correlations.append({
                            "feature_1": col1,
                            "feature_2": col2,
                            "correlation": float(corr_value)
                        })

        patterns["correlations"] = strong_correlations

        return patterns