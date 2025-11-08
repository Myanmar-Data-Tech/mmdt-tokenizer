from typing import List
from .types import Chunk
from .lexicon import FORBID_START


def merge_num_classifier(chunks: List[Chunk]) -> List[Chunk]:
    out: List[Chunk] = []
    i = 0
    n = len(chunks)
    while i < n:
        if chunks[i].tag == "NUM":
            j = i
            while j < n and chunks[j].tag == "NUM":
                j += 1
            if j < n and chunks[j].tag == "CL":
                start = chunks[i].span[0]
                end = chunks[j].span[1]
                merged_text = "".join(c.text for c in chunks[i:j]) + chunks[j].text
                out.append(Chunk((start, end), merged_text, "NUMCL"))
                i = j + 1
                continue
            
            out.extend(chunks[i:j])
            i = j
            continue
        
        out.append(chunks[i])
        i += 1
    return out

def merge_predicate(chunks: List["Chunk"]) -> List["Chunk"]:
    """
    Merge: (RAW, POSTP)+  +  SFP (one or more, closing)  +  optional PUNCT
    → single PRED chunk.

    Examples:
      RAW, PAR, RAW, SFP              -> PRED
      PAR, SFP, SFP, PUNCT            -> PRED
      RAW, RAW, SFP, PUNCT, PUNCT     -> merges up to the first PUNCT only
      RAW, PAR, X                     -> unchanged (no SFP after RAW|PAR run)
    """
    out: List["Chunk"] = []
    i = 0
    n = len(chunks)

    while i < n:
        if(chunks[i].tag in FORBID_START):
            out.append(chunks[i])
            i+=1
            continue
        j = i
        if j < n and chunks[j].tag == "NEG":    j += 1
        if j < n and chunks[j].tag in ("RAW", "POSTP"):
            while j < n and chunks[j].tag in ("RAW", "POSTP"):j += 1
           # SFP (one or more) — require at least one
            had_sfp = False
            while j < n and chunks[j].tag == "SFP":
                had_sfp = True
                j += 1
            # optional neg ending
            had_neg_end = False
            if j < n and chunks[j].tag == "NEG_CLITIC": 
                had_neg_end = True
                j += 1
            
            if had_sfp or had_neg_end:
                if j < n and chunks[j].tag == "PUNCT": j += 1
                start = chunks[i].span[0]
                end = chunks[j - 1].span[1]
                text = "".join(ch.text for ch in chunks[i:j])
                out.append(Chunk((start, end), text, "PRED"))
                i = j
                continue
                
        # fallback passthrough
        out.append(chunks[i])
        i += 1

    return out
