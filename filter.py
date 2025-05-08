import subprocess

def enhance_audio(input_path: str, output_path: str):
    subprocess.run(
        ["python", "-m", "df.enhance", input_path, "-o", output_path],
        check=True
    )

enhance_audio("data/20250508/converted/output_towav_2.wav", "data/20250508/converted/output_filter_2.wav")
