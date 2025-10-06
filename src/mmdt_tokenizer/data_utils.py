import pandas as pd

def standardize_text_input(texts, column=None) -> pd.Series:
    """
    Convert input of various types (DataFrame, Series, list, str) into
    a pandas Series of strings. 
    None values are replaced with empty strings.
    """
    if texts is None:
        raise ValueError("Input 'texts' cannot be None")

    if isinstance(texts, pd.DataFrame):
        if column is None:
            raise ValueError("Please specify 'column' when passing a DataFrame")
        if column not in texts.columns:
            raise ValueError(f"Column '{column}' not found in DataFrame")
        return texts[column].astype(str).fillna("")

    elif isinstance(texts, pd.Series):
        return texts.astype(str).fillna("")

    elif isinstance(texts, list):
        return pd.Series([(str(t) if t is not None else "") for t in texts])

    elif isinstance(texts, str):
        return pd.Series([texts])

    else:
        raise TypeError(f"Unsupported input type: {type(texts)}")

