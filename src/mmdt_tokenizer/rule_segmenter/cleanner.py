from typing import List
from .types import Chunk
from .lexicon import SKIP
from dataclasses import replace

def clean_postp_tag(chunks: List["Chunk"]) -> List["Chunk"]:
    """
    If a 'postp' chunk is preceded by punctuation, change its pos to 'raw'.

    Preceded-by-punctuation includes:
      1) previous chunk's is tagged as POSTP
      2) previous chunk's text ends with punctuation 
      3) the current chunk's text begins with punctuation 
         This covers scripts where punctuation may attach to the token, e.g., Myanmar '၊' '။'.
    """
    out: List["Chunk"] = []
    for i, ch in enumerate(chunks):
        new_ch = replace(ch)

        if ch.tag == "POSTP":
            prev_tag = chunks[i - 1].tag if i > 0 else None
            prev_text = chunks[i -1].text if i > 0 else ""

            is_prec_punct = (i > 0 and prev_tag == "PUNCT")
            is_end_punct = bool(prev_text) and (prev_text[-1] in SKIP)

            cur_text = getattr(ch, "text", "") or ""
            is_start_punct = bool(cur_text) and (cur_text[0] in SKIP)

            if i == 0 or is_prec_punct or is_end_punct or is_start_punct:
                new_ch = replace(ch, tag="RAW")
        
        out.append(new_ch)

    return out


def clean_space_chunk(chunks: List["Chunk"]) -> List["Chunk"]:
    out: List["Chunk"] = []
    for ch in chunks:
        # Skip chunks where text is empty or only spaces
        if not ch.text or ch.text.isspace():
            continue
        out.append(ch)
    return out


def clean_sfp_chunks(chunks: List["Chunk"]) -> List["Chunk"]:
    out: List["Chunk"] = []
    n = len(chunks)

    last_non_punct_idx = None
    for i in reversed(range(n)):
        ch = chunks[i]
        if ch.tag not in ("PUNCT",):  
            last_non_punct_idx = i
            break

    for i, ch in enumerate(chunks):
        if i == last_non_punct_idx and ch.tag in ("CONJ", "VEP"):
            ch.tag = "SFP"
        out.append(ch)

    return out
