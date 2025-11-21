from typing import List
from .types import Chunk
from .lexicon import FUN_TAG


def collapse_to_phrases(chunks):
   
    sentences = []

    def flush():
        if buf:
            surface.append("".join(buf))
            buf.clear()

    for sent in chunks: 
        surface: List[str] = []
        buf: List[str] = []
        for ch in sent:
            tag = getattr(ch, "tag", None)
            txt = getattr(ch, "text", "") 
            
            if tag == "PUNCT":
                # skip punctuation except ။
                if surface and txt == "။": surface[-1] +=txt
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
    
        sentences.append(all_tokens)
    return sentences
