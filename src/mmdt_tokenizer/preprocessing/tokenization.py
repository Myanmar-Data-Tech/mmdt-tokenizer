import re
from typing import List, Dict
from ..patterns import PUNCT_PATTERN, DIGITS, BURMESE_LETTERS

def split_punct(text: str, protected: Dict[str, str]) -> List[str]:
    tokens = []
    for token in text.split():
        if token in protected:
            tokens.append(token)
        else:
            tokens.extend(PUNCT_PATTERN.sub(r" \1 ", token).split())
    return tokens

def separate_letters_digits(text: str) -> str:
    text = re.sub(fr'(?<=[{BURMESE_LETTERS}A-Za-z])(?=[{DIGITS}])', ' ', text)
    return re.sub(fr'(?<=[{DIGITS}])(?=[{BURMESE_LETTERS}A-Za-z])', ' ', text)
