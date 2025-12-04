import re

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
PROTECTED_SPLIT_PATTERN = re.compile(r'(\x02PROT[A-Z]+\x03)')

EMAIL_PATTERN = re.compile(r'([A-Za-z0-9\u1040-\u1049._%+\-]+)\s*@\s*([A-Za-z0-9.\-]+)(?:\.[A-Za-z]{2,})?') #email address
URL_PATTERN = re.compile(r'https?://[^\s]+|www\.[^\s]+') #url link
PER_NAME_PATTERN = re.compile(r'@@?[A-Za-z0-9_]+') #mention for socieal media post

ABB_ENG_PATTERN = re.compile(r'\b(?:[A-Za-z]\.?\s*){2,}[A-Za-z]?\b')
TITLE_PATTERN = re.compile(r'\b(?:Ph\.D|Dr\.|Mr\.|Mrs\.|Ms\.|Prof\.)\b') #tile
ABB_BUR_PATTERN_1 = re.compile(r'(?:[က-အ]\s*[./-]\s*){2,}[က-အ]?')
ABB_BUR_PATTERN_2 = re.compile(r'(?<![\u1000-\u1021\u102B-\u103E])([\u1000-\u1021]{2,})(?=[\s.,\-@/!?]|$)')


DATE_PATTERN_01 = re.compile(
    r'(?:'
    r'[0-9\u1040-\u1049]{1,2}[./\-][0-9\u1040-\u1049]{1,2}[./\-][0-9\u1040-\u1049]{2,4}'  # DD-MM-YYYY
    r'|[0-9\u1040-\u1049]{4}[./\-][0-9\u1040-\u1049]{1,2}[./\-][0-9\u1040-\u1049]{1,2}'  # YYYY-MM-DD
    r'|[0-9\u1040-\u1049]{4}\s*-\s*[0-9\u1040-\u1049]{4}'                              # YYYY–YYYY
    r')'
)

DATE_PATTERN_02 = re.compile(
    r'(?:[0-9\u1040-\u1049]+|(?:တစ်|နှစ်|သုံး|လေး|ငါး|ခြောက်|ခုနစ်|ရှစ်|ကိုး|ဆယ်|ရာ|ထောင်|သိန်း|သန်း)+)\s*(?:ခု(?:နှစ်)?)?\s*'
    r'(?:ဇန်နဝါရီ|ဖေဖော်ဝါရီ|မတ်|ဧပြီ|မေ|ဇွန်|ဇူလိုင်|ဩဂုတ်|အောဂုတ်|စက်တင်ဘာ|အောက်တိုဘာ|နိုဝင်ဘာ|ဒီဇင်ဘာ)\s*(?:လ)?\s*'
    r'(?:[0-9\u1040-\u1049]+|(?:တစ်|နှစ်|သုံး|လေး|ငါး|ခြောက်|ခုနစ်|ရှစ်|ကိုး|ဆယ်|ရာ|ထောင်|သောင်း|သိန်း|သန်း)+)\s*(?:ရက်(?:နေ့)?)?',
    re.UNICODE
)

TIME_PATTERN = re.compile(r'(?:[0-9\u1040-\u1049]{1,2}):(?:[0-9\u1040-\u1049]{2})(?::(?:[0-9\u1040-\u1049]{2}))?')

DEC_NUM_PATTERN = re.compile(r'(?:[0-9\u1040-\u1049]+\.[0-9\u1040-\u1049]+)')  # decimal
LONG_NUM_PATTERN = re.compile(r'[0-9\u1040-\u1049]+(?:[,.][0-9\u1040-\u1049]+)+')  # long number (e.g. ၁,၀၀၀)
FRC_NUM_PATTERN = re.compile(r'[0-9\u1040-\u1049]+/[0-9\u1040-\u1049]+')  # fraction

NUMBER_PATTERN = re.compile(r'^[\d၀-၉]+(?:[,.][\d၀-၉]+)*$') # Numbers (English or Myanmar digits, with , or .)
WORD_NUM_PATTERN = re.compile(
    r'(?<![\u1000-\u1021\u102B-\u103E])'
    r'(?:တစ်|နှစ်|သုံး|လေး|ငါး|ခြောက်|ခုနစ်|ရှစ်|ကိုး|ဆယ်|ရာခိုင်နှုန်း|ရာ|ဆယ့်|ရာ့|ထောင်|ထောင့်|သောင်း|သိန်း|သန်း)'
    r'(?:[\u102B-\u103E]*)(?![\u1000-\u1021\u102B-\u103E])')
PHONE_NUM_PATTERN = re.compile(r'(?:\+?95|09|၀၉)[\s\-]?(?:[0-9\u1040-\u1049][\s\-]?){6,}')

POSSESIVE_PATTERN = re.compile(r"\b\w+'[a-zA-Z]+\b")


TAG_PATTERNS = {
    "NUM": [NUMBER_PATTERN, PHONE_NUM_PATTERN],
    "WORDNUM": [WORD_NUM_PATTERN],
    "ORG": [ABB_BUR_PATTERN_1, ABB_BUR_PATTERN_2, ABB_ENG_PATTERN],
    "NAME": [PER_NAME_PATTERN],
    "DATE": [DATE_PATTERN_01, DATE_PATTERN_02], 
    "TIME": [TIME_PATTERN],
    "EMAIL": [EMAIL_PATTERN], 
    "URL": [URL_PATTERN]
}


PROTECT_PATTERNS =[
    EMAIL_PATTERN, # email address
    URL_PATTERN, # URL
    PER_NAME_PATTERN, #social media mention
    ABB_ENG_PATTERN, # English abbreviation
    TITLE_PATTERN, # titles
    ABB_BUR_PATTERN_1,ABB_BUR_PATTERN_2, # Burmese abbrev (တ.က.က)
    DATE_PATTERN_01, DATE_PATTERN_02, #Date 
    TIME_PATTERN,  # Time
    DEC_NUM_PATTERN, LONG_NUM_PATTERN, FRC_NUM_PATTERN, #Dec, Long, Fraction
    PHONE_NUM_PATTERN, #Phone number
    POSSESIVE_PATTERN, #Possessive (English)
    WORD_NUM_PATTERN, #Burmese Numbers
    NUMBER_PATTERN # Any Number
]


# === syllable break pattern ===

my_consonant = r'က-အ'
en_char = r'a-zA-Z0-9'
other_char = r'ဣဤဦဧဩဪဿ၌၍၏၀-၉၊။!-/:-@[-`{-~\s'
subscript_symbol = r'္'  #U+1039 (ထပ်ဆင့်)
dot_below_symbol = r'့'  #U+1037 (အောက်ကမြင့်)
a_that = r'်' # U+103A athet


SYLLABLE_BREAK_PATTERN = re.compile(
    r"("  
        r"(?<!" + subscript_symbol + r")[" + my_consonant + r"]"
        r"(?![" + a_that + subscript_symbol + r"])"
        r"(?![" + dot_below_symbol + a_that + r"])"
        r"|[" + en_char + other_char + r"]"
        r"|ဥ(?!"+ a_that + r")"
    r")",
    re.UNICODE
)




