"""Generate oss chinese instruct data using oss-instruct method and seeds."""
import json
import logging
import concurrent.futures

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

from utils import extract_code_pattern, extract_lang_pattern

logging.basicConfig(
    filename="oss_zh.log",
    format="%(levelname)s:%(message)s",
    level=logging.INFO,
    encoding="utf-8",
)
logger = logging.getLogger()

PROMPT = """
You are exceptionally skilled at crafting high-quality programming problems and offering precise solutions.
Please gain inspiration from the following random code snippet to create a high-quality programming problem. Present your output in two distinct sections: [Problem Description] and [Solution]. [Problem Description] should be presented in Chinese.

Code snippet for inspiration:
```
{seed}
```

Guidelines for each section:
1. [Problem Description]: This should be **completely self-contained**, providing all the contextual information one needs to understand and solve the problem. Assume common programming knowledge, but ensure that any specific context, variables, or code snippets pertinent to this problem are explicitly included.
2. [Solution]: Offer a comprehensive, **correct** solution that accurately addresses the [Problem Description] you provided.
"""

OPENAI_API_BASE = ""
OPENAI_API_KEY = ""


def generate_oss_zh(idx, llm, seed):
    """generate oss chinese data with a seed using LLM"""
    try:
        message = HumanMessage(content=PROMPT.format(seed=seed))
        res = llm([message])

        problem, solution = res.content.split("[Solution]\n")
        problem = problem.split("[Problem Description]\n")[1]

        code = extract_code_pattern(solution)
        if code is None:
            logging.warning(f"failed on {idx}, seed: {seed}")  # pylint: disable=W1203
            return None

        lang = extract_lang_pattern(code)
        logging.info(f"success on {idx}, seed: {seed}")  # pylint: disable=W1203

        data = {
            "data": "oss_zh",
            "lang": lang,
            "seed": seed,
            "messages": [
                {"role": "user", "content": problem},
                {"role": "assistant", "content": code},
            ],
        }
        return data
    except Exception as e:  # pylint: disable=W0718
        logging.error(f"failed on {idx}, seed: {seed}, error: {e}")  # pylint: disable=W1203
        return None


def main():
    """main function"""
    llm = ChatOpenAI(
        openai_api_base=OPENAI_API_BASE,
        openai_api_key=OPENAI_API_KEY,
        temperature=0.5,
    )

    with open("oss_seeds.json", "r", encoding="utf-8") as f:
        seeds = json.load(f)

    with open("oss_zh.jsonl", "w", encoding="utf-8") as f:
        with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
            futures = [executor.submit(generate_oss_zh, idx, llm, seed) for idx, seed in enumerate(seeds)]

            for future in concurrent.futures.as_completed(futures):
                result = future.result()

                if result is None:
                    # successfully generate oss_zh data
                    f.write(f"{json.dumps(result)}\n")
                    f.flush()


if __name__ == "__main__":
    main()
