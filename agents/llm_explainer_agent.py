import ollama


class LLMExplainerAgent:

    def explain(self, profile, insights, recommendations):

        prompt = f"""
You are an expert data analyst.

Your task is to explain dataset analysis results in a way that a beginner can easily understand.

Use clear, concise language and structure your response using Markdown.

Your explanation MUST follow this format:

## TL;DR
Provide a 2–3 sentence summary of the most important findings.

## Dataset Overview
Briefly explain what the dataset contains.

## Key Relationships
Explain important correlations, patterns, or trends in the data.

## Anomalies or Unusual Findings
Explain any suspicious or unexpected patterns.

## Interpretation
Explain what these findings might mean in real-world terms.

## Suggested Next Steps
Suggest what a data analyst should investigate next.

Here is the analysis information:

Dataset Profile:
{profile}

Insights Detected:
{insights}

Recommendations:
{recommendations}

Important instructions:
- Use simple language
- Avoid technical jargon where possible
- Keep explanations clear and concise
- Write like a human data analyst explaining results
"""

        response = ollama.chat(
            model="mistral-large-3:675b-cloud",
            messages=[{"role": "user", "content": prompt}]
        )

        return response["message"]["content"]