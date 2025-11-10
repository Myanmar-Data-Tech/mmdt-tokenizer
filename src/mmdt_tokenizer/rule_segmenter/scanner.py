from typing import Dict, Tuple, List, Optional
from .lexicon import SKIP
from .types import Chunk


def print_trie(node: dict, prefix: str = "", level: int = 0):
    """Recursively print the trie structure with indentation."""
    indent = "    " * level
    for key, child in node.items():
        if key == "_END_":
            print(f"{indent}└── [END: {child}]")
        else:
            print(f"{indent}├── {key}")
            print_trie(child, prefix + key, level + 1)

def build_trie(patterns: Dict[Tuple[str, ...], str]) -> dict:
    root = {}
    for seq, tag in patterns.items():
        node = root
        if(type(seq) is tuple):
            for s in seq:
                node = node.setdefault(s, {})
        else:
            node = node.setdefault(seq,{})
                
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

    n = len(tokens)
    best_end: Optional[int] = None
    best_tag: Optional[str] = None
    best_text: Optional[str] = None

    for trie, tag_override in pipeline:
        node = trie
        j = i
        last_end: Optional[int] = None
        last_tag: Optional[str] = None
        while j < n:
            t = tokens[j]
            if t in SKIP or t not in node:
                break
            node = node[t]; j += 1
            if "_END_" in node:
                last_end = j - 1
                last_tag = tag_override or node["_END_"]

        if last_end is not None and last_tag is not None:
            if best_end is None or last_end > best_end:
                best_end = last_end
                best_tag = last_tag
                best_text = "".join(tokens[i:last_end + 1])
    
    if best_end is None:
        return None
    assert best_tag is not None
    assert best_text is not None

    return Chunk(span=(i, best_end), text=best_text, tag=best_tag)
   
