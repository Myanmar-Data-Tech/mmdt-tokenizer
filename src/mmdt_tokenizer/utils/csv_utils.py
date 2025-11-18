import pandas as pd
from typing import List, Union

def save_tokens_to_csv(tokens: Union[List[str], List[List[str]]], save_csv: str, conll_style: bool = True):
    """Save tokenized text to CSV (CoNLL-style or sentence-per-row)."""
    if not tokens:
        sublists = []
    elif isinstance(tokens[0], list):
        sublists = tokens
    elif isinstance(tokens, list):
        sublists = [[t] for t in tokens]
    else:
        sublists = [[str(tokens)]]


    if conll_style:
        rows = []
        num_sublists = len(sublists)
        for token_index, sublist in enumerate(sublists):
            string_sublist = [str(token).strip() for token in sublist]
            rows.extend(string_sublist)
            if token_index < num_sublists - 1:
                rows.append("")
        pd.DataFrame({"token": rows}).to_csv(save_csv, index=False, encoding="utf-8-sig")
    else:
        
        df_rows = pd.DataFrame(sublists)
        df_rows.columns = [f"Token_{i+1}" for i in range(df_rows.shape[1])]
        df_rows.to_csv(save_csv, index=False, encoding="utf-8-sig")


    
def save_tags_to_csv(chunks, save_csv_filename):
    if chunks and isinstance(chunks[0], list):
        flat_chunks = [ch for sent in chunks for ch in sent]
    elif chunks:
        flat_chunks = chunks
    else:
        flat_chunks = []
    df = pd.DataFrame(flat_chunks)
    df.to_csv(save_csv_filename, index=False, encoding="utf-8-sig")


    
