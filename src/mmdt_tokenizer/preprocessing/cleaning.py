import re
from ..patterns import PROTECTED_SPLIT_PATTERN, DIGITS

def remove_punct_outside_protected(text: str) -> str:
    return ''.join(
        part if part.startswith("\x02PROT") else re.sub(r'[-:/]', ' ', part)
        for part in PROTECTED_SPLIT_PATTERN.split(text)
    )

def collapse_digit_spaces(text: str) -> str:
    # Times
    text = re.sub(
        fr'([{DIGITS}]{{1,2}})\s*:\s*([{DIGITS}]{{2}})(?:\s*:\s*([{DIGITS}]{{2}}))?',
        lambda m: f"{m.group(1)}:{m.group(2)}" + (f":{m.group(3)}" if m.group(3) else ""),
        text
    )
    # Numbers with separators
    text = re.sub(fr"([{DIGITS}](?:[,.][{DIGITS}]{{3}})+)", lambda m: m.group(0).replace(" ", ""), text)
    
    # Dates
    text = re.sub(fr'([{DIGITS}]{{1,2}})\s*([/\-\.])\s*([{DIGITS}]{{1,2}})\s*([/\-\.])\s*([{DIGITS}]{{2,4}})',
                  r'\1\2\3\4\5', text)
    return text
