from typing import List
from .types import Chunk
from .lexicon import SKIP

FUNCTION_TAGS = {"POSTP","CONJ","SFP","AUX","NEG","NEG_CLITIC","CL","NUMCL","MONTH", "PRN", "REGION"}

def collapse_to_phrases(chunks: List[Chunk]) -> List[str]:
    surface: List[str] = []
    buf: List[str] = []

    def flush():
        if buf:
            surface.append("".join(buf))
            buf.clear()

    for ch in chunks:
        tag = getattr(ch, "tag", None)
        txt = getattr(ch, "text", "")

        if tag == "PUNCT":
            flush()
            surface.append(txt)
        elif tag in FUNCTION_TAGS:
            flush()
            surface.append(txt)
        elif tag == "PRED" or not tag:
            # accumulate normal syllables into a phrase
            buf.append(txt)
        else:
            buf.append(txt)
    flush()
    return [t for t in surface if t]
