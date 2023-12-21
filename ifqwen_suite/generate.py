"""Genereate llm lora results."""
import os
import json
import requests
import argparse

from copy import deepcopy
from tqdm.auto import tqdm

from utils import extract_code_pattern


args_parser = argparse.ArgumentParser()
args_parser.add_argument("-m", "--model", type=str)
args_parser.add_argument("-i", "--input", type=str)
args_parser.add_argument("-o", "--output", type=str)
args = args_parser.parse_args()

URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
HEADERS = {
    "Authorization": f"Bearer {os.getenv('DASHSCOPE_API_KEY')}",
    "Content-Type": "application/json",
}
PAYLOAD = {
    "model": "llm-lora-72b-chat",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": "",
            }
        ]
    },
    "resources": [
        {
            "resource_id": f"{args.model}",
            "resource_type": "llm_lora",
        }
    ],
}


def get_solution(prompt: str) -> str:
    """get solution from model inference"""
    payload = deepcopy(PAYLOAD)
    payload["input"]["messages"][0]["content"] = prompt

    try:
        response = requests.request("POST", URL, headers=HEADERS, data=payload, timeout=3600)
    except Exception:  # pylint: disable=W0718
        return ""

    return response.text


def main():
    """main function"""
    with open(args.input, "r", encoding="utf-8") as fi:
        with open(args.output, "w", encoding="utf-8") as fo:
            for line in tqdm(fi.readlines()):
                line = json.loads(line)
                prompt = line["prompt"]
                test = line["text"]

                solution = get_solution(prompt)
                solution = extract_code_pattern(solution)

                data = {"Solution": solution, "test": test}
                fo.write(f"{json.dumps(data)}\n")


if __name__ == "__main__":
    main()
