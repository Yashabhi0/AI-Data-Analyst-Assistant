import streamlit as st
import os
import shutil
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
• Data Quality Score & Report
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
# Quality Report helpers
# ------------------------------------------------

_GRADE_COLOUR = {
    "Excellent": "🟢",
    "Good":      "🔵",
    "Fair":      "🟡",
    "Poor":      "🔴",
}

_METRIC_LABELS = {
    "missing_values":       "Missing Values",
    "duplicates":           "Duplicates",
    "constant_columns":     "Constant Columns",
    "high_cardinality":     "High Cardinality",
    "outliers":             "Outliers",
    "datatype_consistency": "Datatype Consistency",
    "empty_columns":        "Empty Columns",
}


def _score_colour(score: int) -> str:
    """Return a CSS colour string based on the score band."""
    if score >= 90:
        return "green"
    if score >= 75:
        return "orange"
    if score >= 60:
        return "goldenrod"
    return "red"


def _build_radar_chart(metrics: dict) -> go.Figure:
    """Return a Plotly radar / spider chart for the metric scores."""
    labels = [_METRIC_LABELS.get(k, k) for k in metrics]
    values = list(metrics.values())

    # Close the polygon
    labels_closed = labels + [labels[0]]
    values_closed = values + [values[0]]

    fig = go.Figure(
        go.Scatterpolar(
            r=values_closed,
            theta=labels_closed,
            fill="toself",
            line=dict(color="#4C78A8", width=2),
            fillcolor="rgba(76, 120, 168, 0.25)",
            name="Quality Score",
        )
    )
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100]),
        ),
        showlegend=False,
        margin=dict(l=40, r=40, t=40, b=40),
        height=420,
    )
    return fig


def _build_bar_chart(metrics: dict) -> go.Figure:
    """Return a Plotly horizontal bar chart for the metric scores."""
    labels = [_METRIC_LABELS.get(k, k) for k in metrics]
    values = list(metrics.values())
    colours = [_score_colour(v) for v in values]

    fig = go.Figure(
        go.Bar(
            x=values,
            y=labels,
            orientation="h",
            marker=dict(color=colours),
            text=[f"{v}" for v in values],
            textposition="outside",
        )
    )
    fig.update_layout(
        xaxis=dict(range=[0, 110], title="Score (0–100)"),
        yaxis=dict(autorange="reversed"),
        margin=dict(l=10, r=30, t=10, b=30),
        height=340,
    )
    return fig


def _render_quality_report(report: dict) -> None:
    """Render the full Data Quality Report inside the Streamlit dashboard."""

    if not report:
        st.warning("Quality report is not available.")
        return

    overall   = report.get("overall_score", 0)
    grade     = report.get("grade", "Poor")
    metrics   = report.get("metrics", {})
    warnings  = report.get("warnings", [])
    recs      = report.get("recommendations", [])

    icon = _GRADE_COLOUR.get(grade, "⚪")

    # -- Overall score row --
    col_score, col_grade, col_bar = st.columns([1, 1, 4])

    with col_score:
        st.metric("Overall Quality Score", f"{overall} / 100")

    with col_grade:
        st.metric("Grade", f"{icon} {grade}")

    with col_bar:
        st.progress(overall / 100)

    st.divider()

    # -- Per-metric cards --
    st.markdown("**Metric Breakdown**")

    card_cols = st.columns(len(metrics)) if metrics else []

    for idx, (key, score) in enumerate(metrics.items()):
        label = _METRIC_LABELS.get(key, key)
        colour = _score_colour(score)
        with card_cols[idx]:
            st.markdown(
                f"<div style='text-align:center;'>"
                f"<span style='font-size:1.6rem;font-weight:700;color:{colour};'>{score}</span>"
                f"<br><span style='font-size:0.78rem;color:#666;'>{label}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )

    st.divider()

    # -- Charts side by side --
    st.markdown("**Quality Visualisation**")

    chart_left, chart_right = st.columns(2)

    with chart_left:
        st.markdown("Radar Chart")
        if metrics:
            st.plotly_chart(_build_radar_chart(metrics), use_container_width=True)

    with chart_right:
        st.markdown("Score per Metric")
        if metrics:
            st.plotly_chart(_build_bar_chart(metrics), use_container_width=True)

    st.divider()

    # -- Warnings --
    if warnings:
        st.markdown("**Warnings**")
        for w in warnings:
            st.warning(w)

    # -- Recommendations --
    if recs:
        st.markdown("**Recommendations**")
        for r in recs:
            st.info(r)


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

    df, profile, insights, recommendations, ai_explanation, missing_summary, quality_report = st.session_state["analysis_result"]

    # ------------------------------------------------
    # Data Quality Report
    # ------------------------------------------------
    st.subheader("Data Quality Report")

    _render_quality_report(quality_report)

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