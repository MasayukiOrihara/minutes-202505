import os
from openai import OpenAI
from dotenv import load_dotenv

# .envファイルからAPIキーを読み込み
load_dotenv()
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

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
cut_text = chunks[0]

# === ② ChatGPTで議事録に要約 ===
context1 = "あなたはプロの文章校正者です。グループワークでの会話を書き起こした口語文を会話の流れが分かるように文語文にしてください。"
context2 = "あなたはプロの議事録作成者です。会議中に話された内容を文語にまとめたものを、箇条書きで流れと結論が分かるように要約をしてください。"
context3 = "あなたはプロの議事録作成者です。会議中に話された内容を文語にまとめたものを、大きなトピックに分け箇条書きでまとめてください"
context4 = "あなたはプロの議事録作成者です。会議中に話された内容を文語にまとめたものを、大きなトピックに分け箇条書きでまとめてください。情報が不明瞭で結論に推測が多分に含まれる場合、トピックに注釈を追加してください。"

response =  client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {"role": "system", "content": context4}, # プロンプトによってどう文章いじるか変わる
        {"role": "user", "content": cut_text}
    ],
    temperature=0.3
)

summary = response.choices[0].message.content
print("▼ 議事録：\n", summary)

# === ③ 議事録を外部ファイルに保存 ===
output_file_path = "data/20250509/minutes.txt" # 出力データはここで指定
with open(output_file_path, "w", encoding="utf-8") as f:
    f.write(summary)

print(f"\n議事録を {output_file_path} に保存しました。")
