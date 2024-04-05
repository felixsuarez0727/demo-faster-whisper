import os
import requests
import subprocess

# Define the URLs and file paths
urls = [
    ("https://upload.wikimedia.org/wikipedia/commons/2/22/George_W._Bush%27s_weekly_radio_address_%28November_1%2C_2008%29.oga", "gb0.ogg"),
    ("https://upload.wikimedia.org/wikipedia/commons/1/1f/George_W_Bush_Columbia_FINAL.ogg", "gb1.ogg"),
    ("https://upload.wikimedia.org/wikipedia/en/d/d4/En.henryfphillips.ogg", "hp0.ogg"),
    ("https://cdn.openai.com/whisper/draft-20220913a/micro-machines.wav", "mm1.wav")
]

# Create a directory for the samples
os.makedirs("audios_for_testing", exist_ok=True)

# Download the audio samples
for url, filename in urls:
    response = requests.get(url)
    with open(os.path.join("audios_for_testing", filename), "wb") as f:
        f.write(response.content)

# Convert downloaded OGG files to WAV using ffmpeg
for filename in os.listdir("audios_for_testing"):
    if filename.endswith(".ogg"):
        ogg_path = os.path.join("audios_for_testing", filename)
        wav_path = os.path.join("audios_for_testing", os.path.splitext(filename)[0] + ".wav")
        subprocess.run(["ffmpeg", "-i", ogg_path, "-ar", "16000", "-ac", "1", "-acodec", "pcm_s16le", wav_path], capture_output=True)

print("Audio samples downloaded and converted to .wav successfully.")
