import subprocess
import time

fmt = "Location:%20%l%0ATemperature:%20%t%0APrecipitation:%20%p"
url = f"https://wttr.in/?format={fmt}"

def get_wttr(retries: int = 1, delay: float = 1.0) -> str:
    for attempt in range(retries + 1):
        result = subprocess.run(
            ["curl", "-s", url], capture_output=True, text=True
        )
        if result.returncode == 0:
            return result.stdout.strip()
        if result.returncode == 52 and attempt < retries:
            time.sleep(delay)
            continue
        return f"curl error {result.returncode}"
