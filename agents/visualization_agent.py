import os
import matplotlib.pyplot as plt
import seaborn as sns


class VisualizationAgent:

    def generate(self, df, output_dir="outputs/charts"):

        os.makedirs(output_dir, exist_ok=True)

        numeric_cols = df.select_dtypes(include=["number"]).columns
        categorical_cols = df.select_dtypes(include=["object", "category"]).columns

        # -------------------------------
        # 1. Histogram (Distribution)
        # -------------------------------
        for col in numeric_cols:
            plt.figure()
            sns.histplot(df[col].dropna(), kde=True)
            plt.title(f"Histogram - {col}")
            plt.savefig(f"{output_dir}/{col}_histogram.png")
            plt.close()

        # -------------------------------
        # 2. Box Plot (Outliers)
        # -------------------------------
        for col in numeric_cols:
            plt.figure()
            sns.boxplot(x=df[col])
            plt.title(f"Boxplot - {col}")
            plt.savefig(f"{output_dir}/{col}_boxplot.png")
            plt.close()

        # -------------------------------
        # 3. Correlation Heatmap
        # -------------------------------
        if len(numeric_cols) > 1:
            plt.figure(figsize=(10, 8))
            corr = df[numeric_cols].corr()
            sns.heatmap(corr, annot=True, cmap="coolwarm")
            plt.title("Correlation Heatmap")
            plt.savefig(f"{output_dir}/correlation_heatmap.png")
            plt.close()

        # -------------------------------
        # 4. Bar Charts (Categories)
        # -------------------------------
        for col in categorical_cols:
            if df[col].nunique() < 20:
                plt.figure()
                df[col].value_counts().head(10).plot(kind="bar")
                plt.title(f"Top Categories - {col}")
                plt.savefig(f"{output_dir}/{col}_bar_chart.png")
                plt.close()

        # -------------------------------
        # 5. Scatter Plots (Relationships)
        # -------------------------------
        if len(numeric_cols) >= 2:
            for i in range(len(numeric_cols)):
                for j in range(i + 1, len(numeric_cols)):
                    plt.figure()
                    sns.scatterplot(
                        x=df[numeric_cols[i]],
                        y=df[numeric_cols[j]]
                    )
                    plt.title(f"{numeric_cols[i]} vs {numeric_cols[j]}")
                    plt.savefig(
                        f"{output_dir}/{numeric_cols[i]}_vs_{numeric_cols[j]}_scatter.png"
                    )
                    plt.close()

        # -------------------------------
        # 6. Pair Plot (Full numeric overview)
        # -------------------------------
        if len(numeric_cols) > 1 and len(numeric_cols) <= 6:
            pairplot = sns.pairplot(df[numeric_cols])
            pairplot.fig.suptitle("Pair Plot", y=1.02)
            pairplot.savefig(f"{output_dir}/pairplot.png")
            plt.close()

        # -------------------------------
        # 7. Violin Plot (Distribution shape)
        # -------------------------------
        for col in numeric_cols:
            plt.figure()
            sns.violinplot(x=df[col])
            plt.title(f"Violin Plot - {col}")
            plt.savefig(f"{output_dir}/{col}_violinplot.png")
            plt.close()

        # -------------------------------
        # 8. Boxplot by Category
        # -------------------------------
        for cat_col in categorical_cols:
            if df[cat_col].nunique() < 10:
                for num_col in numeric_cols:
                    plt.figure(figsize=(8, 6))
                    sns.boxplot(x=df[cat_col], y=df[num_col])
                    plt.title(f"{num_col} by {cat_col}")
                    plt.xticks(rotation=45)
                    plt.savefig(
                        f"{output_dir}/{num_col}_by_{cat_col}_boxplot.png"
                    )
                    plt.close()

        # -------------------------------
        # 9. Missing Values Heatmap
        # -------------------------------
        plt.figure(figsize=(10, 6))
        sns.heatmap(df.isnull(), cbar=False)
        plt.title("Missing Values Heatmap")
        plt.savefig(f"{output_dir}/missing_values_heatmap.png")
        plt.close()