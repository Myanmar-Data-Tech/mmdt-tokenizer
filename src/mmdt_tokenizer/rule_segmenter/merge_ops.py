from typing import List, Iterable
from .types import Chunk
from .lexicon import FORBID_TAG


def merge_num_classifier(chunks: List[Chunk]) -> List[Chunk]:
    out: List[Chunk] = []
    i = 0
    n = len(chunks)
    while i < n:
        if chunks[i].tag == "NUM":
            j = i
            while j < n and chunks[j].tag == "NUM":
                j += 1
            start = chunks[i].span[0]
            end = chunks[j-1].span[1]
            merged_text = "".join(c.text for c in chunks[i:j])
            merged_text = merged_text.strip().replace(" ","")
            out.append(Chunk((start, end-1), merged_text, "NUM"))
            i = j 
            continue
        
        out.append(chunks[i])
        i += 1
    return out

def merge_between_boundaries(chunks: List["Chunk"]) -> List["Chunk"]:
    """
    Merge runs of non-forbidden chunks that lie strictly between ANY two boundary chunks,
    where each boundary's pos is in `boundary_values` (e.g., {'conj','postp'}).

    - Keeps boundary chunks as-is (both ends).
    - Inside each boundary-delimited window, concatenates consecutive eligible chunks.
    - Any chunk with a forbidden tag is NOT merged and splits the run.
    - Everything outside boundary windows is passed through unchanged.

    Supported windows include conj...postp, postp...conj, postp...postp, conj...conj.
    """
    boundary_values: Iterable[str] = ("CONJ", "POSTP")
    merged_tag: str = "MERGED"
    boundary_values = set(boundary_values)

    out: List["Chunk"] = []
    i = 0
    n = len(chunks)

    while i < n and chunks[i].tag not in boundary_values:
        out.append(chunks[i])
        i += 1

    while i < n:
        left = chunks[i]
        out.append(left)  # keep left boundary
        i += 1
        
        run: List["Chunk"] = []
        while i < n and chunks[i].tag not in boundary_values:
            ch = chunks[i]
            if ch.tag in FORBID_TAG:
                if run:
                    start = run[0].span[0]
                    end = run[-1].span[1]
                    text = "".join(c.text for c in run if c.text)
                    out.append(Chunk((start, end), text, merged_tag))
                    run.clear()
                out.append(ch)
            else:
                run.append(ch)
            i += 1

        # end scanning 
        if run:
            start = run[0].span[0]
            end = run[-1].span[1]
            text = "".join(c.text for c in run if c.text)
            out.append(Chunk((start, end), text, merged_tag))
            run.clear()

        if i < n and chunks[i].tag in boundary_values:
            out.append(chunks[i])
            i += 1

        # Copy any non-boundary tail (outside any window)
        while i < n and chunks[i].tag not in boundary_values:
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
        if(chunks[i].tag in FORBID_TAG):
            out.append(chunks[i])
            i+=1
            continue
        j = i
        if j < n and chunks[j].tag == "NEG":    j += 1
        if j < n and chunks[j].tag in ("RAW"):
            while j < n and chunks[j].tag in ("RAW"):j += 1
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
                
        out.append(chunks[i])
        i += 1

    return out
