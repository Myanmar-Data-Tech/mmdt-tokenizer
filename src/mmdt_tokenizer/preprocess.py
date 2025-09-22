import re
import pandas as pd
from .constants import PROTECT_SPACES, RE_MM_LETTER_SPACE


def remove_myanmar_spaces(text: str, preserve_digits: bool = False) -> str:
    """Remove spaces between Myanmar syllables, optionally preserving digit spacing."""
    # FIXME: This function can be optimized further.
    if preserve_digits:
        for pattern, replacement in PROTECT_SPACES:
            text = pattern.sub(replacement, text)

    prev = None
    while prev != text:
        prev = text
        text = RE_MM_LETTER_SPACE.sub(r"\1\2", text)

    if preserve_digits:
        text = text.replace("☃", " ")
    return text


def preprocess_text(text: str, mode: str = "my_not_num") -> str:
    """Normalize whitespace and remove unwanted spaces based on mode."""
    # FIXME: This function can be optimized further.
    text = re.sub(r"\s+", " ", text).strip()
    if mode == "all":
        return text.replace(" ", "")
    elif mode == "my":
        return remove_myanmar_spaces(text, preserve_digits=False)
    elif mode == "my_not_num":
        text = remove_myanmar_spaces(text, preserve_digits=True)
        return re.sub(r"(။|၊)\s+", r"\1", text)  # remove space after punctuation
    return text


def normalize_input(texts, column=None) -> pd.Series:
    # FIXME: This function can be optimized further. I got NoneType error here.
    # print(f"Normalizing texts {texts}")
    # print(f"Normalizing input of type {type(texts)}")
    if texts is None:
        raise ValueError("Input 'texts' cannot be None")
    if isinstance(texts, pd.DataFrame):
        if not column:
            raise ValueError("Please specify 'column' for DataFrame input")
        return texts[column].astype(str)
    elif isinstance(texts, pd.Series):
        return texts.astype(str)
    elif isinstance(texts, list):
        return pd.Series([str(t) for t in texts])
    elif isinstance(texts, str):
        return pd.Series([texts])
    else:
        raise TypeError(f"Unsupported input type: {type(texts)}")