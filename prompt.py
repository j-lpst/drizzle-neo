import argparse
import json
import os
import subprocess
from openai import OpenAI

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

def prompt_llm(prompt):
    apikey = os.getenv("OPENAI_API_KEY"),
    if apikey == (None,):
        apikey = ""

    print(server_url)
    client = OpenAI(
        base_url = server_url,
        api_key=str(apikey)
    )
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt1+prompt2+prompt3},
            {"role": "user", "content": prompt},
        ]
    )
    return completion.choices[0].message.content

def main():
    load_config()
    prompt = parse_args()
    print(prompt_llm(prompt))

if __name__ == "__main__":
    main()
