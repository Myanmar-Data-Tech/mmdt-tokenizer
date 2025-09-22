import pandas as pd
from typing import List, Union


def save_tokens_to_csv(tokens: Union[List[str], List[List[str]]], save_csv: str, conll_style: bool = True):
    """Save tokenized text to CSV (CoNLL-style or sentence-per-row)."""
    if tokens and isinstance(tokens[0], list):
        # FIXME: all_tokens is unused
        all_tokens = [tok for sublist in tokens for tok in sublist] 
        sublists = tokens
    else:
        # FIXME: all_tokens is unused
        all_tokens = tokens
        sublists = [tokens]

    if conll_style:
        rows = []
        for sublist in sublists:
            rows.extend(sublist + [""])
        pd.DataFrame({"token": rows}).to_csv(save_csv, index=False, encoding="utf-8-sig")
    else:
        sentences = [" ".join(sublist).strip() for sublist in sublists]
        pd.DataFrame({"Text": sentences}).to_csv(save_csv, index=False, encoding="utf-8-sig")
