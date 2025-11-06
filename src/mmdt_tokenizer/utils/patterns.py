import re

PUNCT_PATTERN = re.compile(r'([\u104A\u104B.,;:\-\(\)\[\]\{\}%/\\\u2010-\u2015])')
PROTECTED_SPLIT_PATTERN = re.compile(r'(\x02PROT[A-Z]+\x03)')


PROTECT_PATTERNS = [
    re.compile(r'([A-Za-z0-9\u1040-\u1049._%+\-]+)\s*@\s*([A-Za-z0-9.\-]+)(?:\.[A-Za-z]{2,})?'), #email address
    re.compile(r'https?://[^\s]+|www\.[^\s]+'), #url link
    re.compile(r'@@?[A-Za-z0-9_]+'), #mention for socieal media post
    re.compile(r'\b(?:[A-Za-z]\s*\.){2,}[A-Za-z]?\b'), #English abbreviaiton
    re.compile(r'\b(?:Ph\.D|Dr\.|Mr\.|Mrs\.|Ms\.|Prof\.)\b'),#title
    re.compile(r'(?:[က-အ]\s*\.){2,}[က-အ]?'), #abbrebiation (တ.က.က)
    re.compile(r'(?<![က-အ])([က-အ]{2,})(?=[\s.,\-@/!?]|$)'),#abbrebiation (အထက)
    re.compile(r'(?:[0-9\u1040-\u1049]{1,2})[./\-](?:[0-9\u1040-\u1049]{1,2})[./\-](?:[0-9\u1040-\u1049]{2,4})'), #date detection
    re.compile(r'(?:[0-9\u1040-\u1049]{1,2}):(?:[0-9\u1040-\u1049]{2})(?::(?:[0-9\u1040-\u1049]{2}))?'), #time detection
    re.compile(r'(?:[0-9\u1040-\u1049]+\.[0-9\u1040-\u1049]+)'), #decimal / number (dot separated)
    re.compile(r'[0-9\u1040-\u1049]+/[0-9\u1040-\u1049]+'), #decimal / number (/ separated)
    re.compile(r'(?:\+?95|09|၀၉)[\s\-]?(?:[0-9\u1040-\u1049][\s\-]?){6,}'), #phone number in MM
    re.compile(r'[0-9\u1040-\u1049]+(?:[,.][0-9\u1040-\u1049]+)+'), #long number
    re.compile(r'[0-9\u1040-\u1049]{2,}'), #any number
    re.compile(r"\b\w+'[a-zA-Z]+\b"), #possessve '
    re.compile(r'(?:တ[\u1000-\u109F]{1,5}တ[\u1000-\u109F]{1,5}|အ[\u1000-\u109F]{1,5}တ[\u1000-\u109F]{1,5}|[\u1000-\u109F]{1,5}ချည်[\u1000-\u109F]{1,5}ချည်)'),
    re.compile(r'(?:[\u1000-\u109F]+|(?:တစ်|နှစ်|သုံး|လေး|ငါး|ခြောက်|ခုနှစ်|ရှစ်|ကိုး|ဆယ်|ရာ|ထောင်|သောင်း|သန်း)+)')
]

# === syllable break pattern ===

my_consonant = r'က-အ'
en_char = r'a-zA-Z0-9'
other_char = r'ဣဤဥဦဧဩဪဿ၌၍၏၀-၉၊။!-/:-@[-`{-~\s'
subscript_symbol = r'္'  #U+1039 virama (subscript)
a_that = r'်' # U+103A athet

SYLLABLE_BREAK_PATTERN = re.compile(
    r"((?<!" + subscript_symbol + r")[" + my_consonant + r"]"
    r"(?![" + a_that + subscript_symbol + r"])"
    + r"|[" + en_char + other_char + r"])",
    re.UNICODE
)



# === Unicode Character Classes ===
MYANMAR_LETTER = r'\u1000-\u109F\uAA60-\uAA7F\uA9E0-\uA9FF\u102B-\u103F\u1037\u1039'
MYANMAR_DIGIT = r'0-9\u1040-\u1049'


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

# Precompiled regex patterns 
PUNCT_PATTERN = re.compile(r'([\u104A\u104B.,;:\-\(\)\[\]\{\}%/\\\u2010-\u2015])') 
NUMBER_PATTERN = re.compile(r'^[\d၀-၉]+(?:[,.][\d၀-၉]+)*$') # Numbers (English or Myanmar digits, with , or .)
PROTECTED_SPLIT_PATTERN = re.compile(r'(\x02PROT[A-Z]+\x03)') 

