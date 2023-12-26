"""Utilities to for data generation."""
import re

from typing import Optional


CODE_PATTERN = re.compile(r"```[\w\W]*?```")
LANG_PATTERN = re.compile(r"```[\w]*")


def extract_code_pattern(data: str) -> Optional[str]:
    """Extract code snippet"""
    codes = CODE_PATTERN.findall(data)

    if len(codes) != 1:
        # find multiple code snippets, may not be a complete solution
        # skip it
        return ""

    return codes[0]


def extract_lang_pattern(data: str) -> str:
    """Extract coding language"""
    if data == "":
        return ""

    lang = LANG_PATTERN.findall(data)[0][3:]

    return lang
