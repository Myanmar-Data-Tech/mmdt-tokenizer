from typing import List
from .types import Chunk
from .lexicon import SKIP, FUN_TAG


def collapse_to_phrases(chunks) -> List[str]:
    surface: List[str] = []
    buf: List[str] = []

    # flatten if is nested
    if chunks and isinstance(chunks[0], list):
        augmented =[]
        for sent in chunks:
            augmented_sent = sent[:]
            augmented_sent.append(Chunk(span=(-1, -1), text="။", tag="EMPTY"))
            augmented.append(augmented_sent)
        flat_chunks = [ch for sent in augmented for ch in sent]
    else:
        flat_chunks = chunks
    

    def flush():
        if buf:
            surface.append("".join(buf))
            buf.clear()


    for ch in flat_chunks:
        tag = getattr(ch, "tag", None)
        txt = getattr(ch, "text", "") 
        
        if tag == "PUNCT":
            # skip punctuation except ။
            flush()
            continue

        if tag == "EMPTY":
            # add ။ to the last text
            if surface: surface[-1] +=txt
            flush()
            continue

        if tag in ("CONJ", "POSTP"):
            # Merge to last text
            if buf: buf.append(txt)
            elif surface: surface[-1] +=txt
            else: surface.append(txt)
            flush()
            continue

        if tag in FUN_TAG:
            flush()
            surface.append(txt)
            continue
        
        buf.append(txt) # raw goes here

    
    # push remaining one
    flush()
    all_tokens = [t for t in surface]
    return all_tokens
