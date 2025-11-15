from typing import List
from .types import Chunk
from .lexicon import SKIP, FUN_TAG
from .lexicon import CONJ, POSTP, SFP, CL, VEP
from .lexicon import MONTH, DAY, PRN, REGION, SNOUN, TITLE, REG
from .scanner import build_trie, scan_longest_at
from .merge_ops import merge_day_classifier, merge_num_classifier, merge_predicate
from .cleanner import clean_postp_tag, clean_sfp_chunks, clean_punt_chunks
from ..preprocessing import preprocess_burmese_text
from ..utils.patterns import TAG_PATTERNS


import pandas as pd


TRIE_CONJ  = build_trie(CONJ)
TRIE_SFP   = build_trie(SFP)
TRIE_VEP   = build_trie(VEP)
TRIE_POST  = build_trie(POSTP)
TRIE_UNIT  = build_trie(CL)

TRIE_MONTH = build_trie(MONTH)
TRIE_DAY = build_trie(DAY)
TRIE_REGION   = build_trie(REGION)
TRIE_REG   = build_trie(REG)
TRIE_SNOUN  = build_trie(SNOUN)
TRIE_TITLE   = build_trie(TITLE)
TRIE_PRN   = build_trie(PRN)



PIPELINE = [

    (TRIE_REGION,  "REGION"),
    (TRIE_MONTH, "MONTH"),
    (TRIE_DAY, "DAY"),
    (TRIE_REG,  "REG"),
    (TRIE_SNOUN, "SNOUN"),
    (TRIE_TITLE,  "TITLE"),
    (TRIE_PRN,  "PRN"),

    (TRIE_CONJ,  "CONJ"),
    (TRIE_SFP,   "SFP"),
    (TRIE_VEP,   "VEP"),
    (TRIE_POST,  "POSTP"),
    (TRIE_UNIT,  "CL"),   
    
]

def _check_pre_defined_tag(token: str):
    for tag, patterns in TAG_PATTERNS.items():
        if any(p.match(token) for p in patterns):
            return tag
    return None


def _flatten_if_nested(syl_tokens):
    if syl_tokens and isinstance(syl_tokens[0], list):
        flat = []
        for grp in syl_tokens: flat.extend(grp)
        return flat
    return syl_tokens or []


def rule_segment(text: str, protect: bool, get_syllabus):
    # 1) get syllables
    if protect: 
        phrase_tokens, protected = preprocess_burmese_text(text)  
        tokens = []
        for phrase in phrase_tokens:
            if phrase in protected:
                tokens.append(protected[phrase])
            else:
                syllable_tokens = _flatten_if_nested(get_syllabus(phrase))
                syllable_tokens.append(' ')
                tokens.extend(syllable_tokens)
    else:
        tokens = _flatten_if_nested(get_syllabus(text))  
    
    # 2) single pass labeling (priority + longest-match)
    chunks: List[Chunk] = []
    i = 0; n = len(tokens)
    while i < n:
        t = tokens[i]
        if t in SKIP:
            chunks.append(Chunk((i,i), t, "PUNCT")); i += 1; continue
        tag = _check_pre_defined_tag(t)
        if tag: 
            chunks.append(Chunk((i,i), t, tag)); i += 1; continue
        m = scan_longest_at(tokens, i, PIPELINE)
        
        if m:
            chunks.append(m); i = m.span[1] + 1
        else:
            chunks.append(Chunk((i,i), t, "RAW")); i += 1
   
    
    # 3) clean 
    
    chunks = clean_postp_tag(chunks)

    chunks = clean_sfp_chunks(chunks)
  
    # 4) structural merges

    chunks = merge_day_classifier(chunks)
    
    chunks = merge_num_classifier(chunks)
    
    chunks = merge_predicate(chunks)
    
    chunks = clean_punt_chunks(chunks)

    return chunks
