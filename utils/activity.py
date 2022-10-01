def read_content(filename: str):
    with open(filename, "r", encoding='utf-8') as f:
        text = f.read()
    return text
