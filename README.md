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
├── loaders
├── outputs
│
├── dashboard.py
├── orchestrator.py
├── main.py
├── requirements.txt
└── README.md

```

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