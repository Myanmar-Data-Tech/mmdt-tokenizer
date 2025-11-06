from typing import List
from .types import Chunk
import re


def merge_num_classifier(chunks: List[Chunk]) -> List[Chunk]:
    out: List[Chunk] = []
    i = 0
    while i < len(chunks):
        c = chunks[i]
        if c.tag == "RAW" and c.text.isdigit():
            if i+1 < len(chunks) and chunks[i+1].tag == "CL":
                
                start = c.span[0]; end = chunks[i+1].span[1]
                out.append(Chunk((start,end), c.text + chunks[i+1].text, "NUMCL"))
                i += 2; continue
        out.append(c); i += 1
    return out
"""

MY_DIGITS_RE = re.compile(r'[\u1040-\u1049]+$')
# Basic numerals 1–9 + tens forms (10, 11–19)
MY_NUM_WORD_RE = re.compile(
    r'(?:'
    r'တစ်|နှစ်|သုံး|လေး|ငါး|ခြောက်|ခုနှစ်|ရှစ်|ကိုး'
    r'|ဆယ်|တစ်ဆယ်|ဆယ့်(?:တစ်|နှစ်|သုံး|လေး|ငါး|ခြောက်|ခုနှစ်|ရှစ်|ကိုး)?'
    r')$'
)

def is_myanmar_number_like(text: str) -> bool:
    s = text.strip()
    return bool(MY_DIGITS_RE.fullmatch(s) or MY_NUM_WORD_RE.fullmatch(s))

def merge_num_classifier(chunks: List[Chunk]) -> List[Chunk]:
    out: List[Chunk] = []
    i = 0
    while i < len(chunks):
        c = chunks[i]

        # treat raw/num/word tokens that look like numbers (digits or spelled-out)
        if c.tag in {"RAW", "NUM", "WORD"} and is_myanmar_number_like(c.text):
            j = i + 1
            between = []

            # Skip over whitespace/punct between number and classifier
            while j < len(chunks) and chunks[j].tag in {"WS", "PUNC"}:
                between.append(chunks[j])
                j += 1

            # Merge when the next non-WS token is a classifier
            if j < len(chunks) and chunks[j].tag == "CL":
                start = c.span[0]
                end = chunks[j].span[1]
                merged_text = c.text + "".join(b.text for b in between) + chunks[j].text
                out.append(Chunk((start, end), merged_text, "NUMCL"))
                i = j + 1
                continue

        out.append(c)
        i += 1

    return out

"""
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
