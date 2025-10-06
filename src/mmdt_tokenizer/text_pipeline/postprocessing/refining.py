from typing import List
from .splitting import split_punctuation, split_word_digit, split_english, split_mixed_tokens
from .merging import merge_numbers

def refine_tokens(tokens: List[str]) -> List[str]:
    """
    Refinement pipeline:
    1. Split punctuation
    2. Split word-digit boundaries
    3. Split English tokens
    4. Merge numeric tokens
    5. Split mixed tokens
    """
    tokens = split_punctuation(tokens)
    tokens = split_word_digit(tokens)
    tokens = split_english(tokens)
    tokens = merge_numbers(tokens)
    tokens = split_mixed_tokens(tokens)
    return tokens
