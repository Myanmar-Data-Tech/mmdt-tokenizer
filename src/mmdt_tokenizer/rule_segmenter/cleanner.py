from typing import List
from .types import Chunk
from .lexicon import SKIP
import re


def clean_wordnum_tag(chunks: List["Chunk"]) -> List["Chunk"]:
    """
    Cleaning rules:
    1) Normalize percent word 'ရာခိုင်နှုန်း' (1–3 tokens) -> one INUMCL chunk.
    2) Demote isolated WORDNUM -> RAW.
    """
    PERCENT_WORD = "ရာခိုင်နှုန်း"
    MAX_TOKENS = 5
    COMMON_KEYS_PRE = {'ဦး', "ရက်"}
    out: List["Chunk"] = []
    i = 0
    n = len(chunks)
    while i < n:
        cur = chunks[i]

        # ---------- Rule 1: percent word (possibly split) ----------
        txt = ""
        k = 0
        end = None
        while i + k < n and k < MAX_TOKENS and chunks[i + k].tag != "PUNCT":
            txt += chunks[i + k].text
            k += 1
            if txt == PERCENT_WORD or txt.startswith(PERCENT_WORD):
                end = i + k
                break

        if end is not None:
            span_start = chunks[i].span[0]
            span_end = chunks[end - 1].span[1]
            out.append(Chunk((span_start, span_end), PERCENT_WORD, "INUMCL"))
            i = end
            continue

        # ---------- Rule 2: isolated WORDNUM -> RAW ----------
        final_tag = cur.tag
        if cur.tag == "WORDNUM":
            p = i - 1
            while p >= 0 and chunks[p].tag == "PUNCT":p -= 1
            q = i + 1
            while q < n and chunks[q].tag == "PUNCT":q += 1
            prev = chunks[p] if p >= 0 else None
            nxt  = chunks[q] if q < n else None

            prev_is_num = (prev is not None and prev.tag in ("NUM", "WORDNUM"))
            next_is_num = (nxt is not None and 
                        (nxt.tag in ("NUM", "WORDNUM", "CL") or nxt.text in COMMON_KEYS_PRE))

            if not prev_is_num and not next_is_num:
                final_tag = "RAW"

        out.append(Chunk(cur.span, cur.text, final_tag))
        i += 1

    return out

def clean_cls_tag(chunks: List["Chunk"]) -> List["Chunk"]:
    out: List["Chunk"] = []
    day_cl = ("နေ့", "ရက်")
    mth_cl =  "လ"
    pnum_cl = ("အကြိမ်", "အနှစ်", "အသက်")

    for i, cur in enumerate(chunks):
        # default: keep original tag
        final_tag = cur.tag

        if cur.tag in ("CL", "VEP") or cur.text in pnum_cl:
            prev_tag = chunks[i - 1].tag if i > 0 else None
            next_tag = chunks[i + 1].tag if i+1<len(chunks) else None

            if prev_tag == "DAY" and cur.text in day_cl:
                final_tag = "DAYCL"
            if prev_tag == "MONTH" and cur.text == mth_cl:
                final_tag = "MONTHCL"

            if next_tag in ("NUM", "WORDNUM") and cur.text in pnum_cl:
                final_tag = "INUMCL"

        out.append(Chunk(cur.span, cur.text, final_tag))

    return out

def clean_postp_tag(chunks: List["Chunk"]) -> List["Chunk"]:
    """
    If a 'postp' chunk is preceded by punctuation, change its pos to 'raw'.

    Preceded-by-punctuation includes:
      1) previous chunk's is tagged as POSTP
      2) previous chunk's text ends with punctuation 
      3) the current chunk's text begins with punctuation 
         This covers scripts where punctuation may attach to the token, e.g., '၊' '။'.
    """
    out: List["Chunk"] = []
    n = len(chunks)
    i = 0
    special_postp = ("ကို", "က", "မှာ", "ရော", "အား")
    while i <n:
        ch = chunks[i]
        if  ch.text in special_postp:
            prev_tag = chunks[i - 1].tag if i-1 > 0 else None
            prev_text = chunks[i -1].text if i-1 > 0 else ""
            prev_prev_tag = chunks[i - 2].tag if i-2 > 0 else None
            prev_prev_text = chunks[i - 2].text if i-2 > 0 else ""
            next_tag = chunks[i + 1].tag if i+1<n else None

            if (i == 0 or next_tag == "RAW" or 
                (prev_tag == "POSTP" and prev_text == ch.text) or
                (prev_tag == "PUNCT" and prev_prev_tag == "POSTP" and prev_prev_text == ch.text)):
                out.append(Chunk(ch.span, ch.text, "RAW"))
                i +=1
                continue
        
        out.append(ch)
        i += 1
    

    return out

def clean_sfp_chunks(chunks: List["Chunk"]) -> List["Chunk"]:
    """
    Rule 1: PRED + NEG_SET_SFP (NOW TAGGED AS CONJ)
    """
    NEG_SENT_SFP = ("နဲ့", "နှင့်", "နှင့်")   
    ISOLATED_SFP_TO_POSTP = {'ပြီ', '၏', 'စေ', 'သည်', 'မည်', 'ပါ'}
    out = []
    i = 0
    n = len(chunks)
    while i < n:
        cur = chunks[i]
        if (cur.tag == "CONJ" and cur.text in NEG_SENT_SFP 
            and len(out) > 0 and out[-1].tag == "PRED"):
            prev = out.pop()               
            merged_span = (prev.span[0], cur.span[1])
            merged_text = prev.text + cur.text
            out.append(Chunk(merged_span, merged_text, "PRED"))
            i += 1
            continue
        q = i + 1
        while q < n and chunks[q].tag == "PUNCT": q += 1
        next_tag = chunks[q].tag if q < n else None
        if cur.tag == "SFP" and cur.text in ISOLATED_SFP_TO_POSTP:
            p = len(out) - 1
            while p >= 0 and out[p].tag == "PUNCT": p -= 1
            prev_tag = out[p].tag if p >= 0 else None
           
            if prev_tag not in ("PRED", "SFP", "VEP") and\
                next_tag not in ("PRED", "SFP"):
                cur = Chunk(cur.span, cur.text, "POSTP")

        if cur.tag == "VEP":
            if next_tag not in ("SFP", "PRED"):
                cur = Chunk(cur.span, cur.text, "RAW")

        out.append(cur)
        i += 1

    return out

def clean_chunks(chunks: List["Chunk"]) -> List["Chunk"]:
    
    cleaned = []
    for ch in chunks:
        ZW_CHARS = r"[\u200b\ufeff\u2060]" 
        new_text = re.sub(ZW_CHARS, "", ch.text)

        if new_text:
            cleaned.append(Chunk(ch.span, new_text, ch.tag))

    return cleaned