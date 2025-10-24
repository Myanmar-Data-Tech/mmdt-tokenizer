import re
from dataclasses import dataclass
from typing import List, Tuple, Dict
from ..utils.constants import PARTICLES, SUFFIXES, CLAUSE_MARKERS
from ..tokenzier.syllable_tokenizer import MyanmarSyllableTokenizer


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

def get_syllabus(text: str)->List[str]:
    syllabus_tokenizer = MyanmarSyllableTokenizer()
    syl_tokens = syllabus_tokenizer.tokenize(text)
    return syl_tokens


def tag_particles_and_suffixes(syl_token_list: list):
   
    tokens = []
    start = 0

    if syl_token_list and isinstance(syl_token_list[0], list):
        syls = syl_token_list[0]          # take inner list if nested [[...]]
    else:
        syls = syl_token_list or []       # ensure list

    syls = [str(s) for s in syls] 

    for index, tok in enumerate(syls):
        if tok in PARTICLES:
            chunk = "".join(syls[start:index+1])
            tokens.append(chunk)
            start = index +1
    
    if start < len(syls):
        chunk = "".join(syls[start:])
        tokens.append(chunk)


    return tokens
    """
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
   """


def detect_clause_boundaries(text: str):
    pass
    """
    boundaries: List[ClauseBoundary] = []
    for m in CLAUSE_MARKERS_RE.finditer(text):
        boundaries.append(ClauseBoundary(m.group(0), m.start(), m.end()))
    return boundaries
    """


def rule_segment(text: str) -> List[str]:
    syl_tokens = get_syllabus(text) #--> return nested list for creating dataframe purpose
    lex_tokens = tag_particles_and_suffixes(syl_tokens)
    clause_bnds = detect_clause_boundaries(text)
    
    return lex_tokens
