import re


def prepare_chunks(content, chunk_size):
    chunks = []
    current_chunk = {
        "content": "",
        "lines": []
    }

    for line in content.splitlines():
        if line.strip() == "":
            continue

        if len(current_chunk['content']) + len(line.rstrip()) + 1 > chunk_size:
            chunks.append(current_chunk)
            current_chunk = {
                "content": "",
                "lines": []
            }

        current_chunk['content'] += line.rstrip() + "\n"
        current_chunk['lines'].append(line.rstrip())

    if current_chunk != "":
        chunks.append(current_chunk)

    return chunks
