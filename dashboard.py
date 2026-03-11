import streamlit as st
import os
import shutil
import pandas as pd
import plotly.express as px

from orchestrator import Orchestrator
from agents.chat_agent import ChatAgent
from agents.storytelling_agent import StorytellingAgent

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
• Missing value handling  
• Insight generation  
• Recommendation generation  
• AI-powered explanation  
• Conversational dataset analysis  
• Automated analysis report
"""
)

# ------------------------------------------------
# Initialize agents
# ------------------------------------------------
orchestrator = Orchestrator()
chat_agent = ChatAgent()
story_agent = StorytellingAgent()

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
# Dataset Summary (for chat)
# ------------------------------------------------
def dataset_summary(df):

    summary = f"""
Rows: {df.shape[0]}
Columns: {df.shape[1]}

Columns:
{list(df.columns)}

Statistics:
{df.describe().to_string()}
"""
    return summary


# ------------------------------------------------
# Run Analysis
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

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        dataset_source = file_path

    elif kaggle_dataset:
        dataset_source = kaggle_dataset

    if dataset_source:

        st.info("Running AI Data Analysis Pipeline...")

        result = orchestrator.run(dataset_source)

        st.session_state["analysis_result"] = result

        st.success("Analysis Complete")

# ------------------------------------------------
# Load Analysis From Session
# ------------------------------------------------
if "analysis_result" in st.session_state:

    df, profile, insights, recommendations, ai_explanation, missing_summary = st.session_state["analysis_result"]

    # ------------------------------------------------
    # AI Explanation
    # ------------------------------------------------
    st.subheader("AI Data Story")

    st.markdown(ai_explanation)

    # ------------------------------------------------
    # Missing Value Handling
    # ------------------------------------------------
    st.subheader("Missing Value Handling")

    missing_df = missing_summary[missing_summary > 0]

    if not missing_df.empty:

        missing_df = missing_df.reset_index()
        missing_df.columns = ["Column", "Missing Values"]

        st.write("Missing values were detected and handled automatically.")
        st.dataframe(missing_df)

        st.info("Numeric columns filled using median. Categorical columns filled using mode.")

    else:
        st.success("No missing values detected in this dataset.")

    # ------------------------------------------------
    # Storytelling Charts
    # ------------------------------------------------
    chart_dir = "outputs/charts"

    if os.path.exists(chart_dir):

        chart_files = sorted(os.listdir(chart_dir))

        st.subheader("Key Insights (AI Selected Charts)")

        try:
            important_charts = story_agent.pick_charts(insights, chart_files)
        except:
            important_charts = chart_files[:3]

        if not important_charts:
            important_charts = chart_files[:3]

        for chart in chart_files[:3]:

            path = os.path.join(chart_dir, chart)

            st.image(path)

    # ------------------------------------------------
    # Show All Charts
    # ------------------------------------------------
    st.subheader("All Generated Visualizations")

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

    # ------------------------------------------------
    # Conversational Dataset Analysis
    # ------------------------------------------------
    st.subheader("Ask AI About This Dataset")

    question = st.text_input("Ask a question about the dataset")

    if question:

        summary = dataset_summary(df)

        answer = chat_agent.ask(summary, question)

        st.markdown(answer)

    # ------------------------------------------------
    # Report
    # ------------------------------------------------
    report_path = "outputs/reports/analysis_report.md"

    if os.path.exists(report_path):

        st.subheader("Analysis Report")

        with open(report_path, "r", encoding="utf-8") as f:
            report = f.read()

        st.markdown(report)

        st.download_button(
            label="Download Report",
            data=report,
            file_name="analysis_report.md",
            mime="text/markdown"
        )