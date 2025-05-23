import math
import os
import subprocess

from openai import OpenAI
from dotenv import load_dotenv

'''

議事録AI「Giron」
ver. 0.1

'''

# パスの指定
input_file_path = "data/20250509/2025OJT3_cut.m4a"
output_file_path = "data/20250509/transcript.txt"
final_file_path = "data/20250509/minutes.txt"

load_dotenv()
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

"""
ファイルサイズ判定
"""
size_megabytes = os.path.getsize(input_file_path) / (1024 * 1024)
max_megabytes = 25

count = math.ceil(size_megabytes / max_megabytes)


"""
カット処理(Whisperは25MBまでしか扱えないため)
whisperで文字起こし
"""
# 総時間取得
def get_audio_duration(file_path):
  result = subprocess.run(
    [
      "ffprobe", "-v", "error",
      "-show_entries", "format=duration",
      "-of", "default=noprint_wrappers=1:nokey=1",
      file_path
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
  )
  return float(result.stdout.strip())

total_duration = get_audio_duration(input_file_path)
segment_duration = math.ceil(total_duration / count)

with open(output_file_path, "w+", encoding="utf-8") as out_f:
  for i in range(count):
    start_time = i * segment_duration
    part_file = f"part_{i+1:03d}.m4a"

    # 分割処理
    subprocess.run([
      "ffmpeg", "-y", "-i", input_file_path,
      "-ss", str(start_time), "-t", str(segment_duration),
      "-c", "copy", part_file
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Whisperで文字起こし
    print(f"文字起こし中: {part_file}")
    with open(part_file, "rb") as audio_file:
      result = client.audio.transcriptions.create(
      model="whisper-1",
      file=audio_file,
      language="ja"
    )
    out_f.write(f"{result.text.strip()}\n\n")

    # 一時ファイルの削除
    os.remove(part_file)
  # 最後に読み込み
  out_f.seek(0)
  transcription_text = out_f.read()


"""
・口語→文語
・要約
"""
# 文字数が長すぎる場合分割をする
def split_text_by_chars(text, max_chars=20000):
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_chars
        chunk = text[start:end]
        chunks.append(chunk)
        start = end
    return chunks

chunks = split_text_by_chars(transcription_text)

# 解決策が浮かぶまで最初の部分のみ
split_text = chunks[0]

# 口語 → 文語
response1 =  client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {"role": "system", "content": "あなたはプロの文章校正者です。グループワークでの会話を書き起こした口語文を会話の流れが分かるように文語文にしてください。"},
        {"role": "user", "content": split_text}
    ],
    temperature=0.2
)
change = response1.choices[0].message.content

# 要約
response2 =  client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {"role": "system", "content": "あなたはプロの議事録作成者です。会議中に話された内容を文語にまとめたものを、大きなトピックに分け箇条書きでまとめてください。情報が不明瞭で結論に推測が多く含まれる場合、トピックに注釈を追加してください。"},
        {"role": "user", "content": change}
    ],
    temperature=0.2
)
summary = response2.choices[0].message.content

with open(final_file_path, "w", encoding="utf-8") as f:
    f.write(summary)

print(f"\n議事録を {final_file_path} に保存しました。")
