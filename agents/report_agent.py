import os


class ReportAgent:

    def generate(self, profile, insights, recommendations, output_dir="outputs/reports"):
        """
        Generates a Markdown report summarizing the dataset analysis.

        Parameters:
            profile (dict)
            insights (list)
            recommendations (list)
            output_dir (str)
        """

        os.makedirs(output_dir, exist_ok=True)

        report_path = os.path.join(output_dir, "analysis_report.md")

        with open(report_path, "w", encoding="utf-8") as f:

            f.write("# AI Data Analyst Report\n\n")

            # Dataset Overview
            f.write("## Dataset Overview\n\n")
            f.write(f"- Rows: {profile.get('rows', 0)}\n")
            f.write(f"- Columns: {profile.get('columns', 0)}\n\n")

            f.write("### Column Names\n")
            for col in profile.get("column_names", []):
                f.write(f"- {col}\n")

            f.write("\n")

            # Data Quality Issues
            f.write("## Data Quality Issues\n\n")

            missing = profile.get("missing_values", {})
            for col, count in missing.items():
                if count > 0:
                    f.write(f"- Column '{col}' has {count} missing values\n")

            duplicates = profile.get("duplicate_rows", 0)
            if duplicates > 0:
                f.write(f"- Dataset contains {duplicates} duplicate rows\n")

            f.write("\n")

            # Insights
            f.write("## Key Insights\n\n")

            for insight in insights:
                f.write(f"- {insight}\n")

            f.write("\n")

            # Recommendations
            f.write("## Recommendations\n\n")

            for rec in recommendations:
                f.write(f"- {rec}\n")

            f.write("\n")

            # Visualizations note
            f.write("## Visualizations\n\n")
            f.write("Generated charts can be found in the `outputs/charts` directory.\n")

        print(f"Report generated: {report_path}")