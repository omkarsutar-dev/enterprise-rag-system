from openai import OpenAI
from app.config import OPENAI_API_KEY, LLM_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_answer(query, context_chunks):
    context = "\n\n".join([chunk["text"] for chunk in context_chunks])

    prompt = f"""
    You are an enterprise AI assistant.
    Answer strictly based on the provided context.

    Context:
    {context}

    Question:
    {query}
    """

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content