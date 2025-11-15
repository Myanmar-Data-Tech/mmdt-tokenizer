from typing import List
from .types import Chunk
from .lexicon import SKIP, FUN_TAG


def collapse_to_phrases(chunks: List[Chunk]) -> List[str]:
    surface: List[str] = []
    buf: List[str] = []
    
    def flush():
        if buf:
            surface.append("".join(buf))
            buf.clear()

    if not chunks:
            return []
    else: chunks = chunks[0] if isinstance(chunks[0], list) else chunks
    for ch in chunks:
        tag = getattr(ch, "tag", None)
        txt = getattr(ch, "text", "")

        if tag in ("PUNCT", "POSTP") :
            flush()
            surface.append(txt)
            continue

        if tag in FUN_TAG:
            flush()
            surface.append(txt)
            continue
        
        buf.append(txt)
    flush()
    all_tokens = [t for t in surface if t not in SKIP]
    return all_tokens
