

MAX_CHAR = 4000
DOCX_SAMPLE = ".\\data\\sample.docx.txt"








def chunk_text(text, max_chars=MAX_CHAR, overlap=1):
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]

    chunks = []
    current = []

    current_size = 0

    for para in paragraphs:
        if current_size + len(para) > max_chars and current:
            chunks.append("\n\n".join(current))

            current = current[-overlap:] if overlap else []
            current_size = sum(len(x) for x in current)

        current.append(para)
        current_size += len(para)

    if current:
        chunks.append("\n\n".join(current))

    return chunks





#------------------------------------------------- main
def main():
    with open(DOCX, "r", encoding="utf-8") as f:
        content = f.read()
        
            




#================================================= entry point
if __name__ == "__main__":
    main()
