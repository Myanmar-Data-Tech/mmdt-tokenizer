import re
from typing import List
from .constants import NUMBER_PATTERN


def merge_numbers(tokens: List[str]) -> List[str]:
    """Merge consecutive number tokens into a single token."""
    merged, i = [], 0
    while i < len(tokens):
        tok = tokens[i]
        if NUMBER_PATTERN.match(tok):
            num_tok = tok
            i += 1
            while i < len(tokens) and re.match(r"^[\d၀-၉.,]+$", tokens[i]):
                num_tok += tokens[i]
                i += 1
            merged.append(num_tok)
        else:
            merged.append(tok)
            i += 1
    return merged


def split_word_number(tokens: List[str]) -> List[str]:
    """Split Myanmar words followed by numbers."""
    new_tokens = []
    for tok in tokens:
        m = re.match(r"([\u1000-\u109F\uAA60-\uAA7F]+)\s+([\d၀-၉][\d၀-၉.,]*)", tok)
        if m:
            new_tokens.extend([m.group(1), m.group(2)])
        else:
            new_tokens.append(tok)
    return new_tokens


def split_english(tokens: List[str]) -> List[str]:
    """Split English tokens into words/punctuation."""
    new_tokens = []
    for tok in tokens:
        if re.search(r"[a-zA-Z]", tok):
            new_tokens.extend(re.findall(r"\w+|[^\w\s]", tok))
        else:
            new_tokens.append(tok)
    return new_tokens


def refine_tokens(tokens: List[str]) -> List[str]:
    """Full refinement pipeline: merge numbers, split word+number, split English."""
    tokens = merge_numbers(tokens)
    tokens = split_word_number(tokens)
    tokens = split_english(tokens)
    return tokens
