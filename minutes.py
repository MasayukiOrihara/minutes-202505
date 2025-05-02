import os
from openai import OpenAI
from dotenv import load_dotenv

# .envファイルからAPIキーを読み込み
load_dotenv()
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

# === ① テキストファイルから読み込む ===
input_file_path = "data/20250502.txt"  # ← ここを変更して読み込むファイルを指定
with open(input_file_path, "r", encoding="utf-8") as f:
    transcription_text = f.read()

# === ② ChatGPTで議事録に要約 ===
response =  client.chat.completions.create(
    model="gpt-4o",  # または "gpt-3.5-turbo"
    messages=[
        {"role": "system", "content": "あなたはプロの議事録作成者です。内容を箇条書きで、簡潔にまとめてください。"},
        {"role": "user", "content": transcription_text}
    ],
    temperature=0.5
)

summary = response.choices[0].message.content
print("▼ 議事録：\n", summary)

# === ③ 議事録を外部ファイルに保存 ===
output_file_path = "minutes.txt"
with open(output_file_path, "w", encoding="utf-8") as f:
    f.write(summary)

print(f"\n議事録を {output_file_path} に保存しました。")
