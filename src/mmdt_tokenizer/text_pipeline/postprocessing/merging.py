from typing import List
from ..patterns import NUMBER_PATTERN

def merge_numbers(tokens: List[str]) -> List[str]:
    """Merge consecutive numeric tokens (Myanmar/English digits, commas, dots)."""
    merged, buf = [], []
    for tok in tokens:
        if NUMBER_PATTERN.match(tok):
            buf.append(tok)
        else:
            if buf:
                merged.append("".join(buf))
                buf = []
            merged.append(tok)
    if buf:
        merged.append("".join(buf))
    return merged
