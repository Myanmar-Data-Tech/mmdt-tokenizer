from typing import List
from .types import Chunk
from .lexicon import SKIP
from .lexicon import CONJ, POSTP, SFP, AUX, NEG_PREFIX, NEG_SUFFIX, MONTHS, CL, PRN, REGION
from .scanner import build_trie, scan_longest_at
from .merge_ops import merge_num_classifier, merge_predicate
from .collapse import collapse_to_phrases

TRIE_CONJ  = build_trie(CONJ)
TRIE_POST  = build_trie(POSTP)
TRIE_SFP   = build_trie(SFP)
TRIE_AUX   = build_trie(AUX)
TRIE_NEGP  = build_trie(NEG_PREFIX)
TRIE_NEGR  = build_trie(NEG_SUFFIX)
TRIE_MONTH = build_trie(MONTHS)
TRIE_UNIT  = build_trie(CL)
TRIE_PRN   = build_trie(PRN)
TRIE_REGION   = build_trie(REGION)



PIPELINE = [
    (TRIE_PRN,  "PRN"),
    (TRIE_REGION,  "REGION"),
    (TRIE_MONTH, "MONTH"),
    (TRIE_UNIT,  "CL"),
    (TRIE_CONJ,  "CONJ"),
    (TRIE_POST,  "POSTP"),
    (TRIE_SFP,   "SFP"),
    (TRIE_AUX,   "AUX"),
    (TRIE_NEGP,  "NEG"),
    (TRIE_NEGR,  "NEG_CLITIC"),

]

def _flatten_if_nested(syl_tokens):
    if syl_tokens and isinstance(syl_tokens[0], list):
        flat = []
        for grp in syl_tokens: flat.extend(grp)
        return flat
    return syl_tokens or []

def rule_segment(text: str, get_syllabus) -> List[str]:
    # 1) syllables
    tokens: List[str] = _flatten_if_nested(get_syllabus(text))

    # 2) single pass labeling (priority + longest-match)
    chunks: List[Chunk] = []
    i = 0; n = len(tokens)
    while i < n:
        t = tokens[i]
        if t in SKIP:
            chunks.append(Chunk((i,i), t, "PUNCT")); i += 1; continue
        m = scan_longest_at(tokens, i, PIPELINE)
        if m:
            chunks.append(m); i = m.span[1] + 1
        else:
            chunks.append(Chunk((i,i), t, "RAW")); i += 1

    # 3) structural merges
    chunks = merge_num_classifier(chunks)
    chunks = merge_predicate(chunks)
    # 4) phrase collapse
    return collapse_to_phrases(chunks)
