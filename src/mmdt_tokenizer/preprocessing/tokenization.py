import re
from typing import List, Dict
from ..utils.patterns import PUNCT_PATTERN, MYANMAR_DIGIT, MYANMAR_LETTER

def split_punct(text: str, protected: Dict[str, str]) -> List[str]:
    tokens = []
    for token in text.split():
        if token in protected:
            tokens.append(token)
        else:
            tokens.extend(PUNCT_PATTERN.sub(r" \1 ", token).split())
    return tokens

def separate_letters_digits(text: str) -> str:
    text = re.sub(fr'(?<=[{MYANMAR_LETTER}A-Za-z])(?=[{MYANMAR_DIGIT}])', ' ', text)
    return re.sub(fr'(?<=[{MYANMAR_DIGIT}])(?=[{MYANMAR_LETTER}A-Za-z])', ' ', text)
