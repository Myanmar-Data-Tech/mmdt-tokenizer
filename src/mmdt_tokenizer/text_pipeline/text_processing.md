---
## Folder Structure

text_pipeline/
│
├── __init__.py
│
├── constants.py           # shared regex constants/patterns
├── helpers.py             # small helper functions
│
├── preprocessing/
│   ├── __init__.py
│   ├── cleaning.py        # normalize, remove punct, collapse spaces
│   ├── protection.py      # protect sensitive patterns (URLs, dates, etc.)
│   ├── tokenization.py    # split punct, separate letters/digits
│   ├── preprocess.py      # main pipeline (preprocess_burmese_text)
│
├── postprocessing/
│   ├── __init__.py
│   ├── merging.py         # merge_numbers
│   ├── splitting.py       # split_punctuation, split_word_digit, split_english, split_mixed_tokens
│   ├── refining.py        # refine_tokens pipeline
│
└── tests/
    ├── test_preprocessing.py
    ├── test_postprocessing.py
    └── test_integration.py
