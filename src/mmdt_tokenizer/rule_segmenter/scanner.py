from typing import Dict, Tuple, List, Optional
from .lexicon import SKIP
from .types import Chunk

def build_trie(patterns: Dict[Tuple[str, ...], str]) -> dict:
    root = {}
    for seq, tag in patterns.items():
        node = root
        for s in seq:
            node = node.setdefault(s, {})
        node["_END_"] = tag
    return root

def scan_longest_at(tokens: List[str], i: int, pipeline: List[tuple]) -> Optional[Chunk]:
    """
    Try all tries (with optional tag override) at position i.
    Return the longest match as a Chunk or None.
    pipeline: [(trie_dict, tag_override_or_None), ...] in priority order.
    """
    if tokens[i] in SKIP:
        return None

    best = None  # (end, tag, text)
    n = len(tokens)
    for trie, tag_override in pipeline:
        node = trie
        j = i; last_end = None; last_tag = None
        while j < n:
            t = tokens[j]
            if t in SKIP or t not in node:
                break
            node = node[t]; j += 1
            if "_END_" in node:
                last_end = j - 1
                last_tag = tag_override or node["_END_"]
        if last_end is not None and (best is None or last_end > best[0]):
            best = (last_end, last_tag, "".join(tokens[i:last_end+1]))
    if best is None:
        return None
    end, tag, text = best
    return Chunk(span=(i, end), text=text, tag=tag)
