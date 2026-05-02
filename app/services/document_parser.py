import re

def parse_document(text):

    sections = []

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    current_heading = None
    current_content = []

    for line in lines:

        # 🎯 Heuristic: short lines = heading
        if len(line.split()) <= 4 and line.istitle():

            # save previous section
            if current_heading:
                sections.append({
                    "heading": current_heading,
                    "content": " ".join(current_content)
                })

            # start new section
            current_heading = line
            current_content = []

        else:
            current_content.append(line)

    # add last section
    if current_heading:
        sections.append({
            "heading": current_heading,
            "content": " ".join(current_content)
        })

    return sections