import subprocess
import os

def convert_to_wav(input_path: str, output_path: str, sample_rate: int = 16000):
  """
  FFmpegを使って音声ファイルを16kHz・モノラルのwavに変換する。
  """

  # 出力フォルダがなければ作成
  os.makedirs(os.path.dirname(output_path), exist_ok=True)

  # FFmpegコマンドの構築
  command = [
    "ffmpeg",
    "-y",                     # 上書き確認無し
    "-i", input_path,         # 入力ファイル
    "-ar", str(sample_rate),  # サンプリングレート変更（例: 16000Hz）
    "-ac", "1",               # モノラルに変換（1チャンネル）
    output_path
  ]

  try:
    subprocess.run(command, check=True)
    print(f"変換成功: {output_path}")
  except subprocess.CalledProcessError as e:
    print(f"FFmpeg変換失敗: {e}")

# 実行
convert_to_wav("data/20250508/2025_ojt_2.m4a", "data/20250508/converted/output_towav_2.wav")