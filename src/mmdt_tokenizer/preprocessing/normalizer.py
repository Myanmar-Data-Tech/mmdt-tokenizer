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


def collapse_digit_spaces(text: str) -> str:
    # Times
    text = re.sub(
        fr'([{MYANMAR_DIGIT}]{{1,2}})\s*:\s*([{MYANMAR_DIGIT}]{{2}})(?:\s*:\s*([{MYANMAR_DIGIT}]{{2}}))?',
        lambda m: f"{m.group(1)}:{m.group(2)}" + (f":{m.group(3)}" if m.group(3) else ""),
        text
    )
    # Numbers with separators
    text = re.sub(fr"([{MYANMAR_DIGIT}](?:[,.][{MYANMAR_DIGIT}]{{3}})+)", lambda m: m.group(0).replace(" ", ""), text)
    
    # Dates
    text = re.sub(fr'([{MYANMAR_DIGIT}]{{1,2}})\s*([/\-\.])\s*([{MYANMAR_DIGIT}]{{1,2}})\s*([/\-\.])\s*([{MYANMAR_DIGIT}]{{2,4}})',
                  r'\1\2\3\4\5', text)
    return text
