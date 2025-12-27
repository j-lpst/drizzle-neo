import argparse
import json
import subprocess

def load_config():
    with open('config.json') as f:
        cfg = json.load(f)
    global server_url, mcp_url, model, prompt1, prompt2, prompt3, memory_model, memory_prompt, memory_maxlines
    server_url = cfg['server']['url']
    mcp_url = cfg['mcp']['url']

    model = cfg['model']['model']
    prompt1 = cfg['model']['prompt1']
    prompt2 = cfg['model']['prompt2']
    prompt3 = cfg['model']['prompt3']

    memory_model = cfg['memory']['model']
    memory_prompt = cfg['memory']['prompt']
    memory_maxlines = cfg['memory']['max_lines']

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--prompt", required=True, help="Prompt to send to the LLM")
    args = parser.parse_args()
    prompt = args.prompt.strip()
    return prompt

def main():
    load_config()
    prompt = parse_args()
    print(prompt)

if __name__ == "__main__":
    main()
