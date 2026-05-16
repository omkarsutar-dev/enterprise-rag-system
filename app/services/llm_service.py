from openai import OpenAI
from app.config import OPENAI_API_KEY
from langchain_openai import ChatOpenAI
from app.utils.response_cleaner import clean_response



llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=OPENAI_API_KEY,
    temperature=0
)

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_text(prompt):

    response = llm.invoke(prompt)

    return response.content

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
Answer based on context.

Rules:
- If exact answer not found → provide closest relevant info
- Mention clearly if specific detail is missing
- Do NOT say "no information" directly
- Do not generate LaTeX, markdown equations, or mathematical formatting.
- Explain formulas in plain English.
- If a formula exists, explain it step-by-step in simple words.

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

    answer = response.choices[0].message.content

    answer = clean_response(answer)

    return answer


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