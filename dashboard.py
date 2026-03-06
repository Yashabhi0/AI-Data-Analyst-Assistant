import streamlit as st
import os
import shutil
import pandas as pd
import plotly.express as px
from orchestrator import Orchestrator

st.set_page_config(page_title="AI Data Analyst Assistant", layout="wide")

# ------------------------------------------------
# Title
# ------------------------------------------------
st.title("AI Data Analyst Assistant")
st.write("Upload a dataset or enter a Kaggle dataset name to generate automatic analysis.")

# ------------------------------------------------
# Sidebar
# ------------------------------------------------
st.sidebar.header("About this Tool")

st.sidebar.write(
"""
This AI Data Analyst automatically performs:

• Dataset profiling  
• Automatic visualizations  
• Pattern detection  
• Insight generation  
• Recommendation generation  
• Automated analysis report
"""
)

# ------------------------------------------------
# Initialize Orchestrator
# ------------------------------------------------
orchestrator = Orchestrator()

# ------------------------------------------------
# Dataset Input
# ------------------------------------------------
st.subheader("Dataset Input")

uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv","xlsx"])
kaggle_dataset = st.text_input("Or enter Kaggle dataset name")

run_analysis = st.button("Run Analysis")

df_preview = None

# ------------------------------------------------
# Dataset Preview
# ------------------------------------------------
if uploaded_file is not None:

    if uploaded_file.name.endswith(".csv"):
        df_preview = pd.read_csv(uploaded_file)

    elif uploaded_file.name.endswith(".xlsx"):
        df_preview = pd.read_excel(uploaded_file)

if df_preview is not None:

    st.subheader("Dataset Preview")

    st.dataframe(df_preview.head(10))

    rows = df_preview.shape[0]
    cols = df_preview.shape[1]
    missing = df_preview.isnull().sum().sum()
    duplicates = df_preview.duplicated().sum()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rows", rows)
    c2.metric("Columns", cols)
    c3.metric("Missing Values", missing)
    c4.metric("Duplicate Rows", duplicates)

# ------------------------------------------------
# Interactive Charts
# ------------------------------------------------
def interactive_chart_explorer(df):

    st.subheader("Interactive Data Explorer")

    numeric_cols = df.select_dtypes(include="number").columns
    categorical_cols = df.select_dtypes(include=["object","category"]).columns

    chart_type = st.selectbox(
        "Choose Chart Type",
        ["Histogram","Scatter","Box","Bar"]
    )

    if chart_type == "Histogram":

        col = st.selectbox("Select column", numeric_cols)
        fig = px.histogram(df, x=col)

        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Scatter":

        col1 = st.selectbox("X axis", numeric_cols)
        col2 = st.selectbox("Y axis", numeric_cols)

        fig = px.scatter(df, x=col1, y=col2)

        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Box":

        col = st.selectbox("Select column", numeric_cols)
        fig = px.box(df, y=col)

        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Bar":

        col = st.selectbox("Category column", categorical_cols)

        counts = df[col].value_counts().reset_index()
        counts.columns = [col,"count"]

        fig = px.bar(counts, x=col, y="count")

        st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------
# Natural Language Queries
# ------------------------------------------------
def natural_language_query(df):

    st.subheader("Ask Questions About Your Dataset")

    query = st.text_input(
        "Example: average salary, max sales, correlation between age and salary"
    )

    if query:

        query = query.lower()

        numeric_cols = df.select_dtypes(include="number").columns

        if "average" in query:

            for col in numeric_cols:
                if col in query:
                    st.write(f"Average {col}: {df[col].mean()}")

        elif "max" in query:

            for col in numeric_cols:
                if col in query:
                    st.write(f"Maximum {col}: {df[col].max()}")

        elif "min" in query:

            for col in numeric_cols:
                if col in query:
                    st.write(f"Minimum {col}: {df[col].min()}")

        elif "correlation" in query:

            for col1 in numeric_cols:
                for col2 in numeric_cols:

                    if col1 in query and col2 in query:

                        corr = df[col1].corr(df[col2])
                        st.write(f"Correlation between {col1} and {col2}: {corr}")

# ------------------------------------------------
# Chart Recommendations
# ------------------------------------------------
def recommend_charts(df):

    st.subheader("Recommended Charts")

    numeric_cols = df.select_dtypes(include="number").columns
    categorical_cols = df.select_dtypes(include=["object","category"]).columns

    if len(numeric_cols) > 0:
        st.write("Histogram recommended for:", list(numeric_cols))

    if len(categorical_cols) > 0:
        st.write("Bar charts recommended for:", list(categorical_cols))

    if len(numeric_cols) > 1:
        st.write("Scatter plots recommended between numeric variables.")

    if df.isnull().sum().sum() > 0:
        st.write("Missing values heatmap recommended.")

# ------------------------------------------------
# Anomaly Explanations
# ------------------------------------------------
def explain_anomalies(df):

    st.subheader("Anomaly Explanations")

    numeric_cols = df.select_dtypes(include="number").columns

    for col in numeric_cols:

        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        outliers = df[(df[col] < lower) | (df[col] > upper)]

        if len(outliers) > 0:

            st.write(f"Column **{col}** contains {len(outliers)} anomalous values.")

            if df[col].max() > upper:
                st.write("Some values are unusually high compared to the normal range.")

            if df[col].min() < lower:
                st.write("Some values are unusually low compared to the normal range.")

            st.write("Possible reasons: rare events, data entry errors, or special cases.")
            st.write("---")

# ------------------------------------------------
# Enable AI Features
# ------------------------------------------------
if df_preview is not None:

    interactive_chart_explorer(df_preview)
    natural_language_query(df_preview)
    recommend_charts(df_preview)
    explain_anomalies(df_preview)

# ------------------------------------------------
# Run Analysis Pipeline
# ------------------------------------------------
if run_analysis:

    shutil.rmtree("outputs/charts", ignore_errors=True)
    shutil.rmtree("outputs/reports", ignore_errors=True)

    os.makedirs("outputs/charts", exist_ok=True)
    os.makedirs("outputs/reports", exist_ok=True)

    dataset_source = None

    if uploaded_file is not None:

        os.makedirs("temp", exist_ok=True)

        file_path = os.path.join("temp", uploaded_file.name)

        with open(file_path,"wb") as f:
            f.write(uploaded_file.getbuffer())

        dataset_source = file_path

    elif kaggle_dataset:
        dataset_source = kaggle_dataset

    if dataset_source:

        st.info("Running AI Data Analysis Pipeline...")

        orchestrator.run(dataset_source)

        st.success("Analysis Complete")

        # ------------------------------------------------
        # Display Charts
        # ------------------------------------------------
        st.subheader("Generated Visualizations")

        chart_dir = "outputs/charts"

        if os.path.exists(chart_dir):

            chart_files = sorted(os.listdir(chart_dir))

            charts_per_row = 3

            for i in range(0, len(chart_files), charts_per_row):

                cols = st.columns(charts_per_row)

                for j in range(charts_per_row):

                    if i + j < len(chart_files):

                        chart_file = chart_files[i + j]
                        chart_path = os.path.join(chart_dir, chart_file)

                        with cols[j]:

                            st.image(chart_path)

                            if "histogram" in chart_file:
                                st.caption("Histogram: Shows distribution of values.")

                            elif "boxplot" in chart_file:
                                st.caption("Boxplot: Shows spread and outliers.")

                            elif "scatter" in chart_file:
                                st.caption("Scatter Plot: Shows relationships between variables.")

                            elif "bar_chart" in chart_file:
                                st.caption("Bar Chart: Shows category frequencies.")

                            elif "heatmap" in chart_file:
                                st.caption("Heatmap: Shows correlations between features.")

        # ------------------------------------------------
        # Report
        # ------------------------------------------------
        report_path = "outputs/reports/analysis_report.md"

        if os.path.exists(report_path):

            st.subheader("Analysis Report")

            with open(report_path,"r",encoding="utf-8") as f:
                report = f.read()

            st.markdown(report)

            st.download_button(
                label="Download Report",
                data=report,
                file_name="analysis_report.md",
                mime="text/markdown"
            )

    else:
        st.warning("Please upload a dataset or enter a Kaggle dataset.")