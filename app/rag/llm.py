from ollama import chat


class LLMService:

    def __init__(
        self,
        model: str = "llama3.2",
    ):
        self.model = model

    def generate(
        self,
        question: str,
        context: str,
    ) -> str:

        prompt = f"""
You are an AI assistant answering questions based on
the provided context.

Use only the information contained in the context.

If the answer cannot be found in the context,
say that you do not have enough information.

Context:
{context}

Question:
{question}

Answer:
"""

        response = chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response["message"]["content"]