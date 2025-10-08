import re

PUNCT_PATTERN = re.compile(r'([\u104A\u104B.,;:\-\(\)\[\]\{\}%/\\\u2010-\u2015])')
PROTECTED_SPLIT_PATTERN = re.compile(r'(\x02PROT[A-Z]+\x03)')

PROTECT_PATTERNS = [
    re.compile(r'([A-Za-z0-9\u1040-\u1049._%+\-]+)\s*@\s*([A-Za-z0-9.\-]+)(?:\.[A-Za-z]{2,})?'),
    re.compile(r'https?://[^\s]+|www\.[^\s]+'),
    re.compile(r'@@?[A-Za-z0-9_]+'),
    re.compile(r'\b(?:[A-Za-z]\s*\.){2,}[A-Za-z]?\b'),
    re.compile(r'\b(?:Ph\.D|Dr\.|Mr\.|Mrs\.|Ms\.|Prof\.)\b'),
    re.compile(r'(?:[က-အ]\s*\.){2,}[က-အ]?'),
    re.compile(r'(?:[0-9\u1040-\u1049]{1,2})[./\-](?:[0-9\u1040-\u1049]{1,2})[./\-](?:[0-9\u1040-\u1049]{2,4})'),
    re.compile(r'(?:[0-9\u1040-\u1049]{1,2}):(?:[0-9\u1040-\u1049]{2})(?::(?:[0-9\u1040-\u1049]{2}))?'),
    re.compile(r'(?:[0-9\u1040-\u1049]+\.[0-9\u1040-\u1049]+)'),
    re.compile(r'[0-9\u1040-\u1049]+/[0-9\u1040-\u1049]+'),
    re.compile(r'(?:\+?95|09|၀၉)[\s\-]?(?:[0-9\u1040-\u1049][\s\-]?){6,}'),
    re.compile(r'[0-9\u1040-\u1049]+(?:[,.][0-9\u1040-\u1049]+)+'),
    re.compile(r'[0-9\u1040-\u1049]{2,}'),
    re.compile(r"\b\w+'[a-zA-Z]+\b"),
]

DIGITS = r'0-9\u1040-\u1049'
BURMESE_LETTERS = r'\u1000-\u109F\uAA60-\uAA7F\uA9E0-\uA9FF\u102B-\u103F\u1037\u1039'
