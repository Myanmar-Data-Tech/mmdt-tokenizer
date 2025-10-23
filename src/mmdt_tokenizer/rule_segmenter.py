import re
from dataclasses import dataclass
from typing import List, Tuple, Dict

MYAN_RANGE = r"\u1000-\u109F"
MYAN_EXTA = r"\uAA60-\uAA7F"
MYAN_EXTB = r"\uA9E0-\uA9FF"
MYAN = f"[{MYAN_RANGE}{MYAN_EXTA}{MYAN_EXTB}]"

PUNCT = r"[၊။,.!?;:~\-\(\)\[\]{}\"]"

SYL_PATTERN = re.compile(
    r"(?:\u1004\u103A\u1039)?"
    r"[\u1000-\u1021]"
    r"[\u103B-\u103E]*"
    r"[\u102B-\u1030\u1032\u1036]*"
    r"[\u1037\u1038]?"
    r"(?:\u103A)?"
    r"(?:\u1039[\u1000-\u1021])?"
)

PARTICLES = ['ကို', 'က', 'မှာ', 'ထဲမှာ', 'ထဲက', 'နဲ့', 'ရဲ့', 'များ', 'တွေ', 'တွင်', 'အား', 'မှ', 'သာ', 'လောက်', 'ပဲ', 'မိန့်', 'ကြ', 'လား', 'တယ်', 'မယ်', 'မလား', 'လည်း', 'ပါ', 'နော်', 'ခင်ဗျာ', 'ဗျာ', 'ဖြစ်ပြီး', 'ပြီးတော့', 'နောက်ပြီး', 'ပြီးနောက်', 'ကြောင့်', 'အတွက်', 'ဆိုတော့', 'လို့', 'ဖြစ်လို့', 'တဲ့အတွက်', 'ပေမဲ့', 'သော်လည်း', 'ရင်', 'ပါက', 'လျှင်', 'ဖို့', 'ဖို့အတွက်']
SUFFIXES = ['များ', 'တွေ', 'လေး', 'ကောင်', 'သား', 'ခြား', 'နဲ့', 'ရဲ့', 'မှ', 'သာ', 'ပဲ']
PREFIXES = []

CLAUSE_MARKERS = ['နောက်ပြီး', 'ပြီးနောက်', 'ဖို့အတွက်', 'ဖြစ်ပြီး', 'ပြီးတော့', 'ဖြစ်လို့', 'တဲ့အတွက်', 'သော်လည်း', 'ကြောင့်', 'ဆိုတော့', 'ပေမယ့်', 'အတွက်', 'ပေမဲ့', 'လျှင်', 'လို့', 'ဖို့', 'ရင်', 'ပါက']
CLAUSE_MARKERS_RE = re.compile("|".join(map(re.escape, CLAUSE_MARKERS)))

@dataclass
class Token:
    text: str
    kind: str
    start: int
    end: int

@dataclass
class ClauseBoundary:
    marker: str
    start: int
    end: int

def find_syllables(text: str) -> List[Token]:
    toks = []
    for m in SYL_PATTERN.finditer(text):
        toks.append(Token(text[m.start():m.end()], "syllable", m.start(), m.end()))
    return toks

def split_chunks(text: str) -> List[Tuple[int, int, str]]:
    chunks = []
    i = 0
    while i < len(text):
        if re.match(r"\s", text[i]) or re.match(PUNCT, text[i]):
            i += 1
            continue
        j = i + 1
        while j < len(text) and not re.match(r"\s", text[j]) and not re.match(PUNCT, text[j]):
            j += 1
        chunks.append((i, j, text[i:j]))
        i = j
    return chunks

def tag_particles_and_suffixes(chunks: List[Tuple[int, int, str]]) -> List[Token]:
    tokens: List[Token] = []
    for s, e, ch in chunks:
        if ch in PARTICLES:
            tokens.append(Token(ch, "particle", s, e))
            continue
        matched_suffix = None
        for suf in sorted(SUFFIXES, key=len, reverse=True):
            if ch.endswith(suf) and len(ch) > len(suf) + 0:
                stem = ch[:len(ch) - len(suf)]
                if re.search(MYAN, stem):
                    tokens.append(Token(stem, "word", s, s+len(stem)))
                    tokens.append(Token(suf, "suffix", s+len(stem), e))
                    matched_suffix = suf
                    break
        if matched_suffix:
            continue
        kind = "word" if re.search(MYAN, ch) else "other"
        tokens.append(Token(ch, kind, s, e))
    return tokens

def detect_clause_boundaries(text: str) -> List[ClauseBoundary]:
    boundaries: List[ClauseBoundary] = []
    for m in CLAUSE_MARKERS_RE.finditer(text):
        boundaries.append(ClauseBoundary(m.group(0), m.start(), m.end()))
    return boundaries

def rule_segment(text: str) -> Dict[str, object]:
    chunks = split_chunks(text)
    lex_tokens = tag_particles_and_suffixes(chunks)
    clause_bnds = detect_clause_boundaries(text)
    syllables = find_syllables(text)
    return {"chunks": chunks, "tokens": lex_tokens, "clause_boundaries": clause_bnds, "syllables": syllables}
