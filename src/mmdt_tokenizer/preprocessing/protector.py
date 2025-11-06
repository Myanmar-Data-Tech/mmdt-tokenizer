from typing import Callable
from ..utils.patterns import PROTECT_PATTERNS

def protect_patterns(text: str, replacer: Callable) -> str:
    
    for pattern in PROTECT_PATTERNS:
        text = pattern.sub(replacer, text)
    
    return text
