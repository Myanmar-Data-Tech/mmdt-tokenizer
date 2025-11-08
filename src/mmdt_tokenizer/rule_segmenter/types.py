from dataclasses import dataclass
from typing import Tuple, List

Span = Tuple[int, int]

@dataclass
class Chunk:
    span: Span
    text: str
    tag: str  # "RAW", "CONJ", "POSTP", "SFP", "PRED", "PUNCT", ...

Surface = List[str]
Chunks = List[Chunk]
