from app.services.llm_service import generate_text


def expand_query(query):

    prompt = f"""
Expand the following query with related search keywords.

Query:
{query}

Return only comma-separated keywords.
"""

    return generate_text(prompt)