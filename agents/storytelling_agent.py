import ollama


class StorytellingAgent:

    def pick_charts(self, insights, chart_list):

        prompt = f"""
You are a data storytelling expert.

These charts were generated from a dataset:

{chart_list}

Insights detected:
{insights}

Choose the 3 most important charts that best explain the dataset.

Return ONLY the filenames.
"""

        response = ollama.chat(
            model="mistral-large-3:675b-cloud",
            messages=[{"role": "user", "content": prompt}]
        )

        return response["message"]["content"]