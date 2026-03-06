class RecommendationAgent:

    def generate(self, profile, patterns, outliers):
        """
        Generates recommendations based on dataset analysis.

        Parameters:
            profile (dict): output from ProfilingAgent
            patterns (dict): output from PatternDetectionAgent
            outliers (dict): output from OutlierDetectionAgent

        Returns:
            list of recommendations
        """

        recommendations = []

        # Handle missing values
        missing = profile.get("missing_values", {})
        for col, count in missing.items():
            if count > 0:
                recommendations.append(
                    f"Consider handling missing values in column '{col}' using imputation or removal."
                )

        # Handle duplicates
        duplicates = profile.get("duplicate_rows", 0)
        if duplicates > 0:
            recommendations.append(
                "Consider removing duplicate rows to improve data quality."
            )

        # Recommendations based on correlations
        correlations = patterns.get("correlations", [])
        for corr in correlations:
            f1 = corr["feature_1"]
            f2 = corr["feature_2"]
            value = corr["correlation"]

            if value > 0:
                recommendations.append(
                    f"'{f1}' may positively influence '{f2}'. Consider analyzing this relationship further."
                )
            else:
                recommendations.append(
                    f"'{f1}' may negatively influence '{f2}'. Investigate potential causes."
                )

        # Outlier handling recommendations
        for col, data in outliers.items():
            count = data["count"]
            if count > 0:
                recommendations.append(
                    f"Column '{col}' has {count} outliers. Consider investigating or treating them."
                )

        if not recommendations:
            recommendations.append(
                "No major issues detected. The dataset appears relatively clean."
            )

        return recommendations