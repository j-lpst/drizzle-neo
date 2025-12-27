import subprocess
from pywhispercpp.examples.assistant import Assistant

# pywhispercpp documentation: https://absadiki.github.io/pywhispercpp/

def on_segment(text: str) -> None:
    print(text)
    subprocess.run(['python3', 'prompt.py', '-p', text])
    print("Listening...")

# Models are saved to ~/.local/share/pywhispercpp/models/
assistant = Assistant(
        model = "base.en",
        silence_threshold = 64,         # Default: 8
        q_threshold = 32,               # Default: 16
        commands_callback=on_segment,
        n_threads=8
)

print("The first prompt may take a long time due to KV cache processing! Please be patient.")

# Listening until Ctrl‑C.
assistant.start()
