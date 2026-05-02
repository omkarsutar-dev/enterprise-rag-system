from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text_from_sections(sections):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = []

    for section in sections:

        texts = splitter.split_text(section["content"])

        for t in texts:
            chunks.append({
                "text": t,
                "heading": section["heading"]
            })

    return chunks