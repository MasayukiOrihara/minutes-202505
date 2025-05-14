# === ① テキストファイルから読み込む ===
input_file_path = "data/20250509/transcript.txt"  # ← ここを変更して読み込むファイルを指定
with open(input_file_path, "r", encoding="utf-8") as f:
    transcription_text = f.read()

# === テキストの分割 ===
def split_text_by_chars(text, max_chars=12000):
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_chars
        chunk = text[start:end]
        chunks.append(chunk)
        start = end
    return chunks

chunks = split_text_by_chars(transcription_text)

for i, chunk in enumerate(chunks):
    
    print(f"Chunk {i+1}（{len(chunk)}文字）:\n", chunk[:100], "...\n")  # 最初の100文字だけ表示