# https://github.com/dot-Justin/BonziBuddy-TTS/blob/main/main.py
import requests
import simpleaudio as sa
import io
from urllib.parse import quote_plus
import sys

text = sys.argv[1]

encoded_text = quote_plus(text)
tts_url = f"https://www.tetyys.com/SAPI4/SAPI4?text={encoded_text}&voice=Adult%20Male%20%232%2C%20American%20English%20(TruVoice)&pitch=140&speed=157"
response = requests.get(tts_url, timeout=10)
if response.status_code == 200:
    with open("/tmp/output.mp3", "wb") as f:
        f.write(response.content)

    wave_obj = sa.WaveObject.from_wave_file(io.BytesIO(response.content))
    
    play_obj = wave_obj.play()
    play_obj.wait_done()
else:
    print(f"Failed to fetch audio: {response.status_code}")
