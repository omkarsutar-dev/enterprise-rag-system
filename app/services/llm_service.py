from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_answer(query, context_chunks, history):

    context = "\n".join([c["text"] for c in context_chunks])

    messages = []

    # Add history
    for msg in history:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    # Add current query with context
    messages.append({
        "role": "user",
        "content": f"""
Use the context below to answer:

Context:
{context}

Question:
{query}
"""
    })

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    return response.choices[0].message.content


def generate_streaming_answer(query, context_chunks, history):

    context = "\n".join([c["text"] for c in context_chunks])

    messages = []

    # Add history
    for msg in history:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    messages.append({
        "role": "user",
        "content": f"""
Use the context below to answer:

Context:
{context}

Question:
{query}
"""
    })

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content