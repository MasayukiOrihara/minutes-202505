from openai import OpenAI
from dotenv import load_dotenv
import os

"""
whisperによる文字起こし
"""

# .envの読み込み
load_dotenv()

# OpenAIのAPIキー
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

# 保存先のパス
file_path = "data/20250509/output_raw1_.txt"

# 音声ファイルを開く
with open("data/20250509/2025OJT1_008.m4a", "rb") as audio_file:
  transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    language="ja" # 日本語音声
  )

# ファイルに書き込む
with open(file_path, 'w', encoding='utf-8') as file:
  file.write(transcript.text)

# 結果を表示
print("ファイルが出力されました！")