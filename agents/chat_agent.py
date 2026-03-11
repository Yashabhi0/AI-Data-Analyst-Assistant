import ollama


class ChatAgent:

    def ask(self, dataframe_summary, question):

        prompt = f"""
You are a professional data analyst.

A user is asking questions about a dataset.

Dataset summary:
{dataframe_summary}

User question:
{question}

Answer clearly and simply.
If possible, explain relationships in the data.
"""

        response = ollama.chat(
            model="mistral-large-3:675b-cloud",
            messages=[{"role": "user", "content": prompt}]
        )

        return response["message"]["content"]