# AI Data Analyst Assistant

AI Data Analyst Assistant is a tool that automatically analyzes datasets, generates visualizations, explains insights in human language, and allows users to ask questions about their data.

It combines automated exploratory data analysis (EDA) with AI-powered explanations using a cloud-hosted large language model.

---

## Features

- Automated dataset profiling
- Automatic visualizations (histograms, scatter plots, heatmaps, etc.)
- Pattern and anomaly detection
- Automatic missing value handling
- AI-generated explanations of insights
- Conversational dataset analysis
- Data storytelling with highlighted charts
- Downloadable analysis report
- **Data Quality Report** — automated quality scoring with warnings and recommendations

---

## Tech Stack

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- Streamlit
- Scikit-learn
- Ollama (Cloud)
- Mistral Large 3 LLM

---

## Project Structure

```

AI-Data-Analyst-Assistant
│
├── agents
│   ├── quality_agent.py        ← Data Quality Score agent
│   └── ...
├── loaders
├── outputs
├── utils
│   └── quality_metrics.py      ← Quality metric functions
│
├── dashboard.py
├── orchestrator.py
├── main.py
├── requirements.txt
└── README.md

```

---

## Data Quality Report

After every analysis run, the assistant automatically scores your dataset's quality on a scale of **0 – 100** and displays a full report in the dashboard.

### How the score is calculated

The overall score is a weighted average of seven individual metrics:

| Metric | Weight | What is measured |
|---|---|---|
| Missing Values | 30 % | Percentage of NaN cells across the entire dataset |
| Duplicates | 20 % | Percentage of duplicate rows |
| Outliers | 15 % | Percentage of rows containing at least one IQR outlier |
| Datatype Consistency | 15 % | Object columns that look numeric, or contain mixed types |
| Constant Columns | 10 % | Columns with only one unique (non-null) value |
| Empty Columns | 10 % | Columns that are entirely NaN |
| High Cardinality | — | Categorical columns where ≥ 90 % of values are unique (advisory only) |

Each metric is scored 0 – 100 individually. The weighted sum is clamped to [0, 100].

### Grade bands

| Score | Grade |
|---|---|
| 90 – 100 | 🟢 Excellent |
| 75 – 89 | 🔵 Good |
| 60 – 74 | 🟡 Fair |
| 0 – 59 | 🔴 Poor |

### Dashboard sections

- **Overall score** — displayed via `st.metric` and a progress bar
- **Metric cards** — colour-coded score for each of the seven metrics
- **Radar chart** — spider/polar chart showing all metric scores at once
- **Bar chart** — horizontal bar chart with per-metric colour coding
- **Warnings** — plain-language description of every detected issue
- **Recommendations** — actionable steps to improve data quality

### New files

| File | Purpose |
|---|---|
| `agents/quality_agent.py` | `QualityAgent` class — orchestrates all checks, builds warnings and recommendations |
| `utils/quality_metrics.py` | Pure functions for each metric; `compute_overall_score()` with the weight table |

---

## Installation

Clone the repository:

```

git clone [https://github.com/Yashabhi0/AI-Data-Analyst-Assistant.git](https://github.com/Yashabhi0/AI-Data-Analyst-Assistant.git)
cd AI-Data-Analyst-Assistant

```

Create a virtual environment:

```

python -m venv venv

```

Activate the environment:

```

venv\Scripts\activate

```

Install dependencies:

```

pip install -r requirements.txt

```

---

## Run the Application

```

streamlit run dashboard.py

```

---

## Example Dataset

You can analyze Kaggle datasets like:

```

zynicide/wine-reviews

```

---

## Example Questions for AI

```

Why are sales increasing?
Which variable affects revenue the most?
Explain the anomalies in this dataset.

```

---

## Author

Yashwanth Abhishek
```