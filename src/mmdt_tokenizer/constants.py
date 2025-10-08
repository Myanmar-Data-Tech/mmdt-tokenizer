import re
from pathlib import Path

# === File Paths ===
PROJECT_ROOT = Path(__file__).resolve().parent

DATA_DIR =  PROJECT_ROOT /  "data"
DICT_FILE_PATH = DATA_DIR / "myg2p_mypos.dict"

# === Unicode Character Classes ===
MYANMAR_LETTER = r'[\u1000-\u109F\uAA60-\uAA7F]'
MYANMAR_DIGIT = r'[\u1040-\u1049]'

# Regex patterns for space handling
RE_MM_LETTER_SPACE = re.compile(rf'({MYANMAR_LETTER})\s+({MYANMAR_LETTER})')
RE_MM_DIGIT_DIGIT = re.compile(rf'({MYANMAR_DIGIT})\s+({MYANMAR_DIGIT})')
RE_MM_DIGIT_LETTER = re.compile(rf'({MYANMAR_DIGIT})\s+({MYANMAR_LETTER})')
RE_MM_LETTER_DIGIT = re.compile(rf'({MYANMAR_LETTER})\s+({MYANMAR_DIGIT})')

PROTECT_SPACES = [
    (RE_MM_DIGIT_DIGIT, r'\1☃\2'),
    (RE_MM_DIGIT_LETTER, r'\1☃\2'),
    (RE_MM_LETTER_DIGIT, r'\1☃\2'),
]

# Numbers (English or Myanmar digits, with , or .)
NUMBER_PATTERN = re.compile(r'^[\d၀-၉]+(?:[,.][\d၀-၉]+)*$')

my_consonant = r'က-အ'
other_char_no_num = r'ဣဤဥဦဧဩဪဿ၌၍၏၊။!-/:-@[-`{-~\s'  # Symbols, punctuation, space
subscript_symbol = r'္'
a_that = r'်'

# --- Improved BREAK_PATTERN ---
BREAK_PATTERN = re.compile(
    r"((?<!" + subscript_symbol + r")[" + my_consonant + r"]"
    r"(?![" + a_that + subscript_symbol + r"])"
    + r"|[" + other_char_no_num + r"])",
    re.UNICODE
)


# my_consonant = r'က-အ'
en_char = r'a-zA-Z0-9'
other_char = r'ဣဤဥဦဧဩဪဿ၌၍၏၀-၉၊။!-/:-@[-`{-~\s'
#subscript_symbol = r'္'
# a_that = r'်'

SYLLABLE_BREAK_PATTERN = re.compile(
    r"((?<!" + subscript_symbol + r")[" + my_consonant + r"]"
    r"(?![" + a_that + subscript_symbol + r"])"
    + r"|[" + en_char + other_char + r"])",
    re.UNICODE
)
