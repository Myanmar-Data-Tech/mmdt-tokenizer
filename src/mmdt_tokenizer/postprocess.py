import re
from typing import List
from .constants import NUMBER_PATTERN, PUNCT_PATTERN, SPLIT_PATTERN

def merge_numbers(tokens: List[str]) -> List[str]:
    """Merge consecutive numeric tokens (Myanmar/English digits, commas, dots)."""
 
    merged, buf = [], []
    join_buf, append = "".join, merged.append

    for tok in tokens:
        if NUMBER_PATTERN.match(tok):
            buf.append(tok)
        else:
            if buf:
                append(join_buf(buf))
                buf = []
            append(tok)
    if buf:
        append(join_buf(buf))

    return merged

def split_punctuation(tokens: List[str]) -> List[str]:
    """
    Split standalone punctuation (-၊။()) from tokens.
    Keeps numbers with internal commas/dots intact.
    """
    result = []
    append = result.append
    for tok in tokens:
        if PUNCT_PATTERN.search(tok):
            # split, keeping punctuation as separate tokens
            parts = PUNCT_PATTERN.split(tok)
            puncts = PUNCT_PATTERN.findall(tok)
            # FIXME: handle edge cases with leading/trailing punctuation
            for i, part in enumerate(parts):
                if part:
                    result.append(part)
                if i < len(puncts):
                    result.append(puncts[i])
        else:
            result.append(tok)
    return result




def split_word_digit(tokens: List[str]) -> List[str]:
    """
    Split tokens so that any Burmese/ASCII number stays as a single token
    and is not attached to adjacent letters.  No digit-by-digit fallback.
    """
    out: List[str] = []
    for tok in tokens:
        # handle tokens that already contain spaces
        for sub in re.split(r'\s+', tok):
            if not sub:
                continue
            parts = SPLIT_PATTERN.findall(sub)
            # if nothing matched (rare), keep the whole subtoken unchanged
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

def split_mixed_tokens(tokens: list) -> list:
    """
    Split tokens that contain both Burmese and English (or numbers) into separate tokens.
    Keeps Burmese-only tokens intact.
    """
    result = []
    for tok in tokens:
        # If token contains any English letters
        if re.search(r'[a-zA-Z]', tok):
            # Split into English words and non-ASCII chunks
            parts = re.findall(r'[a-zA-Z]+|[^\x00-\x7F]+', tok)
            result.extend(parts)
        else:
            result.append(tok)
    return result

def refine_tokens(tokens: List[str]) -> List[str]:
    """
    Full refinement pipeline: merge numbers, split word+number, split English.
    This function need to optimize and fix to handle numbers splitting scenerio
    """
    # 1. Split punctuation first
    tokens = split_punctuation(tokens)
    # # 2. Split word-digit boundaries
    # tokens = split_word_digit(tokens) # need to optimize later
    # 3. Split English words
    # tokens = split_english(tokens)
    # print(f"after split english{tokens}")
    # tokens = merge_numbers(tokens)
    return tokens



