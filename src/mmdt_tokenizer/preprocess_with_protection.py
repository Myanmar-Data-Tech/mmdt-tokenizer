import re
import unicodedata
from typing import Tuple, Dict, List
from .preprocess import preprocess_text

def _int_to_letters(n: int) -> str:
    """Convert integer to letters for placeholders (A, B, ..., AA, AB, ...)"""
    s = ""
    while True:
        s = chr(ord('A') + (n % 26)) + s
        n = n // 26 - 1
        if n < 0:
            break
    return s

def split_punct(text: str, protected: Dict[str, str]) -> List[str]:
    """
    Split punctuation as separate tokens, but keep protected placeholders intact.
    """
    # Before splitting on whitespace, make placeholders separated by spaces so .split() sees them as tokens
    text = re.sub(r'(\x02PROT[A-Z]+\x03)', r' \1 ', text)

    punct_pattern = r'([\u104A\u104B\.\,\;\:\-\(\)\[\]\{\}%/\\\u2010-\u2015])'
    parts = []
    for token in text.split():
        if token in protected:
            parts.append(token)
        else:
            token_parts = re.sub(punct_pattern, r" \1 ", token).split()
            parts.extend(token_parts)
    return parts

def protect_patterns(text: str, protect) -> str:
    """Apply protection for various patterns: emails, URLs, numbers, dates, etc."""
    # Emails
    text = re.sub(r'([A-Za-z0-9\u1040-\u1049._%+\-]+)\s*@\s*([A-Za-z0-9.\-]+)(?:\.[A-Za-z]{2,})?', protect, text)
    # URLs
    text = re.sub(r"https?://[^\s]+|www\.[^\s]+", protect, text)
    # Mentions
    text = re.sub(r"@@?[A-Za-z0-9_]+", protect, text)
    # English abbreviations C.E.O / T.O.P
    text = re.sub(r"\b(?:[A-Za-z]\s*\.){2,}[A-Za-z]?\b", protect, text)
    # Academic titles
    text = re.sub(r"\b(?:Ph\.D|Dr\.|Mr\.|Mrs\.|Ms\.|Prof\.)\b", protect, text)
    # Burmese abbreviations like ပ.အ.ဖ
    text = re.sub(r"(?:[က-အ]\s*\.){2,}[က-အ]?", protect, text)
    # # Define a Burmese syllable cluster (base consonant + optional stacked signs/medials/tones)
    # burmese_syllable = r"[က-အ](?:[\u102B-\u103F\u1060-\u109F])*"
    # # Protect Burmese abbreviations like ပ.အ.ဖ or ယူ.အက်စ်.အေ
    # text = re.sub(rf"(?:{burmese_syllable}\s*\.){{2,}}{burmese_syllable}?", protect, text)
    
    # Dates
    text = re.sub(r"(?:[0-9\u1040-\u1049]{1,2})[./\-](?:[0-9\u1040-\u1049]{1,2})[./\-](?:[0-9\u1040-\u1049]{2,4})", protect, text)
    # Times
    text = re.sub(r"(?:[0-9\u1040-\u1049]{1,2}):(?:[0-9\u1040-\u1049]{2})(?::(?:[0-9\u1040-\u1049]{2}))?", protect, text)
    # Decimals
    text = re.sub(r"(?:[0-9\u1040-\u1049]+\.[0-9\u1040-\u1049]+)", protect, text)
    # # Fractions
    # text = re.sub(r"[0-9\u1040-\u1049]+/[0-9\u1040-\u1049]+", protect, text)
    # Phone numbers
    text = re.sub(r"(?:\+?95|09|၀၉)[\s\-]?(?:[0-9\u1040-\u1049][\s\-]?){6,}", protect, text)
    # Multi-digit numbers with thousands separators
    #text = re.sub(r'[0-9\u1040-\u1049]{1,3}(?:\s*[,.]\s*[0-9\u1040-\u1049]{3})+', protect, text)
    text = re.sub(r'[0-9\u1040-\u1049]+(?:[,.][0-9\u1040-\u1049]+)+', protect, text)
    # Plain multi-digit numbers without thousands separators
    text = re.sub(r'[0-9\u1040-\u1049]{2,}', protect, text)
    # English contractions
    text = re.sub(r"\b\w+'[a-zA-Z]+\b", protect, text)

    return text

def remove_punct_outside_protected(text: str) -> str:
    """Remove -, :, / outside protected placeholders"""
    parts = re.split(r'(\x02PROT[A-Z]+\x03)', text)
    return ''.join(
        part if part.startswith("\x02PROT") else re.sub(r'[-:/]', ' ', part)
        for part in parts
    )


def separate_letters_digits(text: str, protected: Dict[str,str]) -> str:
    digits = r'0-9\u1040-\u1049'
    # # Cover: consonants, extensions, vowels, tones, asat, virama, etc.
    # burmese_letters = r'\u1000-\u109F\uAA60-\uAA7F\uA9E0-\uA9FF\u102B-\u103F\u1037\u1039'

    # cover base letters and the common Myanmar combining marks / medials
    burmese_letters = (
        r'\u1000-\u109F'      # Myanmar block
        r'\uAA60-\uAA7F'      # Myanmar extended-A
        r'\uA9E0-\uA9FF'      # Myanmar extended-B
        r'\u102B-\u103E'      # vowels, medial signs, etc.
        r'\u1037\u1038'       # anusvara/visarga-like, etc.
        r'\u1039\u103A'       # virama/asat
        r'\u1050-\u109F'      # other extension area
    )
    # use that in regex char-class:
    burmese_letters_class = fr'{burmese_letters}'


    # Insert space between letter → digit
    text = re.sub(fr'(?<=[{burmese_letters_class}A-Za-z])(?=[{digits}])', ' ', text)
    # Insert space between digit → letter
    text = re.sub(fr'(?<=[{digits}])(?=[{burmese_letters_class}A-Za-z])', ' ', text)

    return text


def collapse_digit_spaces(text: str) -> str:
    """Collapse spaces around digit separators and dates/times"""
    # Times
    text = re.sub(
        r'([0-9\u1040-\u1049]{1,2})\s*:\s*([0-9\u1040-\u1049]{2})(?:\s*:\s*([0-9\u1040-\u1049]{2}))?',
        lambda m: f"{m.group(1)}:{m.group(2)}" + (f":{m.group(3)}" if m.group(3) else ""),
        text
    )
    # Multi-digit numbers
    text = re.sub(r"([0-9\u1040-\u1049](?:[,.][0-9\u1040-\u1049]{3})+)", lambda m: m.group(0).replace(" ", ""), text)
    # Dates
    text = re.sub(
        r'([0-9\u1040-\u1049]{1,2})\s*([/\-\.])\s*([0-9\u1040-\u1049]{1,2})\s*([/\-\.])\s*([0-9\u1040-\u1049]{2,4})',
        r'\1\2\3\4\5', text
    )
    return text

# -------------------------------
# Main Function
# -------------------------------

def preprocess_burmese_text(text: str) -> Tuple[List[str], Dict[str,str]]:
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    # Step 0: Normalize and clean
    # text = unicodedata.normalize("NFKC", text.strip())
    #text = re.sub(r"[~^*_+=<>\[\]{}|\\…“”‘’「」『』\"'#()]+|\.\.+", " ", text)
   
    text = re.sub(r"[~^*_+=<>\[\]{}|\\…“”‘’「」『』\"'#]+|\.\.+", " ", text)

    text = re.sub(r'[\u200B\u200C\u200D\uFEFF]', '', text)
    text = re.sub(r'\s+', ' ', text)

    # Apply same space removal behavior as preprocess_text with given mode
    text = preprocess_text(text)

    # Step 1: Collapse spaces around digits/dates/times
    text = collapse_digit_spaces(text)

    # Step 2: Protect patterns
    protected = {}
    counter = 0
    def protect(m):
        nonlocal counter
        key = f"\x02PROT{_int_to_letters(counter)}\x03"
        protected[key] = m.group(0)
        counter += 1
        # return f" {key} "
        return key
    text = protect_patterns(text, protect)

    # # Step 3: Remove unwanted punctuation outside protected
    text = remove_punct_outside_protected(text)

    # Step 4: Separate letters and digits
    text = separate_letters_digits(text, protected)

    # Step 5: Split punctuation
    tokens = split_punct(text, protected)

    # Step 6: Final cleanup
    tokens = [t for t in tokens if t.strip()]

    return tokens, protected
