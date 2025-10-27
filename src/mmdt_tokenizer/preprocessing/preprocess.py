import re
import unicodedata
from typing import Tuple, Dict, List

from ..utils.text_utils import _int_to_letters
from .normalizer import split_punct, separate_letters_digits, collapse_digit_spaces
from .cleaner import remove_punct_outside_protected
from .protector import protect_patterns

def preprocess_burmese_text(text: str) -> Tuple[List[str], Dict[str, str]]:
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    # Step 0: Normalize and clean
    text = unicodedata.normalize("NFKC", text.strip())
    text = re.sub(r"[~^*_+=<>\[\]{}|\\…“”‘’「」『』\"'#()]+|\.\.+", " ", text)
    text = re.sub(r'[\u200B\u200C\u200D\uFEFF]', '', text)
    text = re.sub(r'\s+', ' ', text)

    # Step 1: Collapse digit/date/time spacing
    text = collapse_digit_spaces(text)

    # Step 2: Protect patterns--> (protection module)
    protected: Dict[str, str] = {}
    counter = 0

    def protect(m: re.Match) -> str:
        nonlocal counter
        key = f"\x02PROT{_int_to_letters(counter)}\x03"
        protected[key] = m.group(0)
        counter += 1
        return f" {key} "

    text = protect_patterns(text, protect) 

    # Step 3: Remove unwanted punctuation outside protected (cleaning module)
    text = remove_punct_outside_protected(text)

    # Step 4: Separate letters and digits (tokenization module)
    text = separate_letters_digits(text)

    # Step 5: Split punctuation (tokenzization module)
    tokens = split_punct(text, protected)

    # Step 6: Cleanup
    tokens = [t for t in tokens if t.strip()]
    return tokens, protected
