import os
import json
import datetime

def chunk_text(text, max_tokens=1000):
    words = text.split()
    chunks, current = [], []
    for w in words:
        current.append(w)
        if len(" ".join(current)) > max_tokens:
            chunks.append(" ".join(current[:-1]))
            current = [w]
    if current: chunks.append(" ".join(current))
    return chunks

def process_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    text_chunks = []
    current_section = "Introduction"
    current_chunk = ""

    for line in lines:
        if line.startswith('#'):
            if current_chunk:
                text_chunks.append((current_section, current_chunk.strip()))
            current_section = line.strip().lstrip('#').strip()
            current_chunk = ""
        else:
            current_chunk += line

    if current_chunk:
        text_chunks.append((current_section, current_chunk.strip()))

    return text_chunks

def process_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [("General", f.read())]

def main():
    output_file = 'dataset.jsonl'
    root_dir = 'learning-materials'
    processed_files = 0
    total_chunks = 0
    seen_chunks = set()

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for subdir, _, files in os.walk(root_dir):
            for file in files:
                file_path = os.path.join(subdir, file)
                processed_chunks = []
                if file.endswith('.md'):
                    processed_chunks = process_markdown(file_path)
                    processed_files += 1
                elif file.endswith('.txt'):
                    processed_chunks = process_text(file_path)
                    processed_files += 1

                for section, text in processed_chunks:
                    chunks = chunk_text(text)
                    for chunk in chunks:
                        if not chunk or chunk in seen_chunks:
                            continue
                        seen_chunks.add(chunk)
                        total_chunks += 1
                        data = {
                            "text": chunk,
                            "metadata": {
                                "source_file": file_path,
                                "section": section,
                                "language": "en",
                                "created_at": datetime.datetime.now().isoformat()
                            }
                        }
                        outfile.write(json.dumps(data, ensure_ascii=False) + '\n')

    print(f"Processed {processed_files} files.")
    print(f"Generated {total_chunks} unique chunks.")

if __name__ == '__main__':
    main()
