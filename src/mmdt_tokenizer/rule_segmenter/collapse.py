from typing import List
from .types import Chunk
from .lexicon import SKIP


def collapse_to_phrases(chunks: List[Chunk], FUNCTION_TAGS) -> List[str]:
    surface: List[str] = []
    buf: List[str] = []

    def flush():
        if buf:
            surface.append("".join(buf))
            buf.clear()

    for ch in chunks:
        tag = getattr(ch, "tag", None)
        txt = getattr(ch, "text", "")

        if tag in ("PUNCT", "POSTP") :
            flush()
            surface.append(txt)
            continue

        if tag in FUNCTION_TAGS:
            flush()
            surface.append(txt)
            continue
        
        buf.append(txt)
    flush()

    return [t for t in surface if t]
