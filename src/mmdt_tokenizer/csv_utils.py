import pandas as pd
from typing import List, Union


def save_tokens_to_csv(tokens: Union[List[str], List[List[str]]], save_csv: str, conll_style: bool = True):
    """Save tokenized text to CSV (CoNLL-style or sentence-per-row)."""
    if not tokens:
        sublists = []
    elif isinstance(tokens[0], list):
        sublists = tokens
    elif isinstance(tokens, list):
        sublists = [tokens]
    else:
        raise TypeError("Input 'tokens' must be List[str] or List[List[str]].")
 
    if conll_style:
        rows = []
        num_sublists = len(sublists)
        for token_index, sublist in enumerate(sublists):
            string_sublist = [str(token) for token in sublist]
            rows.extend(string_sublist+[""])
            if token_index < num_sublists - 1:
                rows.append("")
        pd.DataFrame({"token": rows}).to_csv(save_csv, index=False, encoding="utf-8-sig")
    else:
        sentences = [" ".join([str(token) for token in sublist]).strip() for sublist in sublists]
        pd.DataFrame({"Text": sentences}).to_csv(save_csv, index=False, encoding="utf-8-sig")
