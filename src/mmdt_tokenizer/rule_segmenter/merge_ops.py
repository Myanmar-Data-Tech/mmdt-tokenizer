from typing import List
from .types import Chunk
import re


def merge_num_classifier(chunks: List[Chunk]) -> List[Chunk]:
    out: List[Chunk] = []
    i = 0
    n = len(chunks)
    while i < n:
        c = chunks[i]
        print(c)
        if c.tag == "NUM":
            if i+1 < len(chunks) and chunks[i+1].tag == "CL":
                start = c.span[0]; end = chunks[i+1].span[1]
                out.append(Chunk((start,end), c.text + chunks[i+1].text, "NUMCL"))
                i += 2; continue
        out.append(c); i += 1
    print("end")
    return out

def merge_predicate(chunks: List[Chunk]) -> List[Chunk]:
    out: List[Chunk] = []; i = 0; n = len(chunks)
    while i < n:
        j = i
        if j < n and chunks[j].tag == "NEG": j += 1
        if j < n and chunks[j].tag == "RAW":
            j += 1
            while j < n and chunks[j].tag == "AUX": j += 1
            while j < n and chunks[j].tag in ("SFP","POL","Q"): j += 1
            if j < n and chunks[j].tag == "NEG_CLITIC": j += 1
            start = chunks[i].span[0]; end = chunks[j-1].span[1]
            text = "".join(ch.text for ch in chunks[i:j])
            out.append(Chunk((start,end), text, "PRED"))
            i = j; continue
        out.append(chunks[i]); i += 1
    return out
