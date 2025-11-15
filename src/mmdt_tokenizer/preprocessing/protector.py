from typing import Callable
from ..utils.patterns import PROTECT_PATTERNS
import re

PLACEHOLDER_RE = re.compile(r'\x02[^\x03]*\x03')

def sub_outside_placeholders(text: str, pattern: re.Pattern, repl) -> str:
    parts = []
    last = 0
    for m in PLACEHOLDER_RE.finditer(text):

        seg = text[last:m.start()]
        seg = re.sub(pattern, repl, seg)
        parts.append(seg)

        parts.append(m.group(0))
        last = m.end()

    tail = re.sub(pattern, repl, text[last:])
    parts.append(tail)

    return ''.join(parts)

def protect_patterns(text: str, replacer: Callable) -> str:
    
    for pattern in PROTECT_PATTERNS:
        text = pattern.sub(replacer, text)
    
    return text
