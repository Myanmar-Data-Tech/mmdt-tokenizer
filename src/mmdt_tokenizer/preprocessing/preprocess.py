import re
from typing import Tuple, Dict, List

from .normalizer import split_punct, collapse_digit_spaces
from .cleaner import remove_punct_outside_protected
from .protector import protect_patterns


SAFE_CHARS = ''.join(chr(c) for c in range(0x10, 0x20) if c not in (0x0a, 0x0d))

def _encode_counter(n: int) -> str:
    if n == 0:
        return SAFE_CHARS[0]
    base = len(SAFE_CHARS)
    out = []
    while n > 0:
        n, r = divmod(n, base)
        out.append(SAFE_CHARS[r])
    return ''.join(reversed(out))



def preprocess_burmese_text(text: str) -> Tuple[List[str], Dict[str, str]]:
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")
    # Step 1: Clean text
    text = re.sub(r"[~^*_+=<>\[\]{}|\\…“”‘’「」『』\"'#()]+|\.\.+", " ", text) #remove special characters
    text = re.sub(r'[\u200B\u200C\u200D\uFEFF]', '', text) #remove ghost characters
    text = re.sub(r'\s+', ' ', text) #shrink space
    
    # Step 2: Collapse digit/date/time spacing
    text = collapse_digit_spaces(text)
   
    # Step 3: Protect patterns--> (protection module)
    protected: Dict[str, str] = {}
    counter = 1
    
    def protect(m: re.Match) -> str:
        nonlocal counter
        key = f"\x02{_encode_counter(counter)}\x03"  # no letters/digits
        protected[key] = m.group(0)
        counter += 1
        return f" {key} "
    
    text = protect_patterns(text, protect) 
    
    # Step 4: Remove unwanted punctuation outside protected (cleaning module)
    text = remove_punct_outside_protected(text)

    # Step 5: Split punctuation (normalizer module)
    tokens = split_punct(text, protected)

    # Step 6: Cleanup
    tokens = [t for t in tokens if t.strip()]

    return tokens, protected
