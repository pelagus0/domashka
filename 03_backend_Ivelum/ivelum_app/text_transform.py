from __future__ import annotations

import re

WORD_RE = re.compile(r"([A-Za-zА-Яа-яЁё]{6})(?!™)")


def add_trademark_to_six_letter_words(text: str) -> str:
    return WORD_RE.sub(r"\1™", text)

