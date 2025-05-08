import torchaudio
print(torchaudio.get_audio_backend())  # 例: 'sox_io'

torchaudio.info("data/20250508/converted/output_towav_2.wav")
