import re
from ..utils.patterns import PROTECTED_SPLIT_PATTERN, MYANMAR_DIGIT

def remove_punct_outside_protected(text: str) -> str:
    return ''.join(
        part if part.startswith("\x02PROT") else re.sub(r'[-:/]', ' ', part)
        for part in PROTECTED_SPLIT_PATTERN.split(text)
    )

