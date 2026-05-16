import re


def clean_response(text):

    # Remove LaTeX blocks
    text = re.sub(r"\\\[|\\\]", "", text)

    # Remove \text{}
    text = re.sub(r"\\text\{(.*?)\}", r"\1", text)

    # Replace LaTeX operators
    text = text.replace("\\times", "×")
    text = text.replace("\\frac", "")
    text = text.replace("\\left", "")
    text = text.replace("\\right", "")

    # Remove curly braces
    text = text.replace("{", "")
    text = text.replace("}", "")

    # Remove excessive slashes
    text = text.replace("\\", "")

    # Remove multiple spaces/newlines
    text = re.sub(r"\s+", " ", text)

    return text.strip()