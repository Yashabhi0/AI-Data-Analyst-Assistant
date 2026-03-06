class InsightAgent:

    def generate(self, profile, patterns, outliers):
        """
        Generates human-readable insights from dataset analysis.

        Parameters:
            profile (dict): output from ProfilingAgent
            patterns (dict): output from PatternDetectionAgent
            outliers (dict): output from OutlierDetectionAgent

        Returns:
            list of insights
        """

        insights = []

        # Dataset overview insight
        rows = profile.get("rows", 0)
        cols = profile.get("columns", 0)

        insights.append(f"The dataset contains {rows} rows and {cols} columns.")

        # Missing values insight
        missing = profile.get("missing_values", {})
        for col, count in missing.items():
            if count > 0:
                insights.append(f"Column '{col}' contains {count} missing values.")

        # Duplicate rows insight
        duplicates = profile.get("duplicate_rows", 0)
        if duplicates > 0:
            insights.append(f"The dataset contains {duplicates} duplicate rows.")

        # Correlation insights
        correlations = patterns.get("correlations", [])

        for corr in correlations:
            f1 = corr["feature_1"]
            f2 = corr["feature_2"]
            value = corr["correlation"]

            if value > 0:
                insights.append(
                    f"There is a strong positive correlation ({value:.2f}) between '{f1}' and '{f2}'."
                )
            else:
                insights.append(
                    f"There is a strong negative correlation ({value:.2f}) between '{f1}' and '{f2}'."
                )

        # Outlier insights
        for col, data in outliers.items():
            count = data["count"]
            if count > 0:
                insights.append(f"Column '{col}' contains {count} potential outliers.")

        return insights