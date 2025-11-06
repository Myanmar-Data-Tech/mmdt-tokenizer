import re
from typing import Tuple, Dict, List

from .normalizer import split_punct, collapse_digit_spaces
from .cleaner import remove_punct_outside_protected
from .protector import protect_patterns

def _int_to_letters(n: int) -> str:
    """Convert integer to letters for placeholders (A, B, ..., AA, AB, ...)."""
    chars = []
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        chars.append(chr(ord('A') + remainder))
    return "".join(reversed(chars))

def preprocess_burmese_text(text: str) -> Tuple[List[str], Dict[str, str]]:
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")
    
    text = re.sub(r"[~^*_+=<>\[\]{}|\\…“”‘’「」『』\"'#()/]+|\.\.+", " ", text) #remove special characters
    text = re.sub(r'[\u200B\u200C\u200D\uFEFF]', '', text) #remove ghost characters
    text = re.sub(r'\s+', ' ', text) #shrink space
 

    # Step 2: Collapse digit/date/time spacing
    text = collapse_digit_spaces(text)

    # Step 3: Protect patterns--> (protection module)
    protected: Dict[str, str] = {}
    counter = 0

    def protect(m: re.Match) -> str:
        nonlocal counter
        key = f"\x02PROT{_int_to_letters(counter)}\x03"
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
