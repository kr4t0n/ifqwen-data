"""Calculate pass rate for given results."""
import json
import argparse
import subprocess

args_parser = argparse.ArgumentParser()
args_parser.add_argument("-f", "--file", type=str)
args = args_parser.parse_args()


def main():
    """main function"""
    pkgs = [
        "import math",
        "import re",
        "import sys",
        "import copy",
        "import datetime",
        "import itertools",
        "import collections",
        "import heapq",
        "import statistics",
        "import functools",
        "import hashlib",
        "import numpy",
        "import numpy as np",
        "import string",
        "import unittest",
        "from typing import *",
        "from collections import *",
    ]
    pkgs = "\n".join(pkgs)
    entrance = "if __name__ == '__main__':\n    unittest.main()"

    success, failed = 0, 0
    with open(args.file, encoding="utf-8") as f:
        for line in f.readlines():
            line = json.loads(line)

            solution = line["Solution"]
            test = line["test"]

            code = f"{pkgs}\n{solution}\n{test}\n{entrance}"
            with open("temp.py", "w", encoding="utf-8") as f:
                f.write(code)

            try:
                subprocess.run(["python", "temp.py"], check=True, capture_output=True, text=True, timeout=60)
                success += 1
            except Exception:  # pylint: disable=W0718
                failed += 1

    print(f"pass rate: {success * 1.0 / (success + failed)}")


if __name__ == "__main__":
    main()
