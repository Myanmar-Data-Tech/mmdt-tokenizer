import re
from typing import List
from ..utils.patterns import PUNCT_PATTERN, PROTECTED_SPLIT_PATTERN

def split_punctuation(tokens: List[str]) -> List[str]:
    """Split standalone punctuation, keeping numbers intact."""
    result = []
    for tok in tokens:
        if PUNCT_PATTERN.search(tok):
            parts = PUNCT_PATTERN.split(tok)
            puncts = PUNCT_PATTERN.findall(tok)
            for i, part in enumerate(parts):
                if part:
                    result.append(part)
                if i < len(puncts):
                    result.append(puncts[i])
        else:
            result.append(tok)
    return result

def split_word_digit(tokens: List[str]) -> List[str]:
    """Split tokens so numbers and words are separated."""
    out: List[str] = []
    for tok in tokens:
        for sub in re.split(r'\s+', tok):
            if not sub:
                continue
            parts = PROTECTED_SPLIT_PATTERN.findall(sub)
            out.extend(parts if parts else [sub])
    return out

def split_english(tokens: List[str]) -> List[str]:
    """Split English tokens into words/punctuation."""
    new_tokens = []
    for tok in tokens:
        if re.search(r"[a-zA-Z]", tok):
            new_tokens.extend(re.findall(r"\w+|[^\w\s]", tok))
        else:
            new_tokens.append(tok)
    return new_tokens

def split_mixed_tokens(tokens: List[str]) -> List[str]:
    """Split tokens containing both Burmese and English."""
    result = []
    for tok in tokens:
        if re.search(r'[a-zA-Z]', tok):
            result.extend(re.findall(r'[a-zA-Z]+|[^\x00-\x7F]+', tok))
        else:
            result.append(tok)
    return result
