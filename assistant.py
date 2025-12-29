import subprocess
import multiprocessing
from pywhispercpp.examples.assistant import Assistant

num_threads = multiprocessing.cpu_count()
num_threads = int(num_threads/2)

# pywhispercpp documentation: https://absadiki.github.io/pywhispercpp/
# list of available models: https://absadiki.github.io/pywhispercpp/#pywhispercpp.constants.AVAILABLE_MODELS
# model benchmarks: https://github.com/ggml-org/whisper.cpp/discussions/3074
# model documentation: https://github.com/openai/whisper/blob/main/README.md

def on_segment(text: str) -> None:
    print(text)
    subprocess.run(['python3', 'prompt.py', '-p', text])
    print("--- Listening... ---")

# models are saved to ~/.local/share/pywhispercpp/models/
# pick optimal model (above for list of models) based on your CPU's processing time
# good models based on CPUs I've tested:
# i7-3632QM: base.en
# i7-8650U:  small
assistant = Assistant(
        model = "small",
        silence_threshold = 64,         # Default: 8
        q_threshold = 32,               # Default: 16
        commands_callback = on_segment,
        n_threads = num_threads 
)

print("--- The first prompt may take a long time due to KV cache processing and model downloading! Please be patient. ---")

# Listening until Ctrl‑C.
assistant.start()
