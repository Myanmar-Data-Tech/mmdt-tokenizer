from typing import List
from .types import Chunk
from .lexicon import SKIP, FUN_TAG


def collapse_to_phrases(chunks) -> List[str]:
    surface: List[str] = []
    buf: List[str] = []
    
    def flush():
        if buf:
            surface.append("".join(buf))
            buf.clear()

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

    # FIXED ME : #Noun Phrase (FUN_TAG + POSTP/ CONJ - one word)

    for ch in flat_chunks:
        tag = getattr(ch, "tag", None)
        txt = getattr(ch, "text", "") 
        
        if tag == "PUNCT":
            flush()
            surface.append(txt)
            continue

        if tag == "CONJ":
            flush()
            surface.append(txt+" ")
            continue

        if tag == "POSTP":
            if buf: buf.append(txt + " ")
            elif surface: surface[-1] +=txt + " "
            else: surface.append(txt + " ")
            continue


        if tag in FUN_TAG:
            flush()
            surface.append(txt)
            continue
        
        if tag == "EMPTY":
            flush()
            surface.append(txt)
            continue
        
        buf.append(txt)
    
    # push remaining one
    flush()
    all_tokens = [t for t in surface]
    return all_tokens
