## mmdt-tokenizer
A Myanmar text tokenizer library (“mmdt-tokenizer”) for word- and syllable-level tokenization, normalization, and preprocessing. Useful for processing Burmese , mixed text, numbers, and English segments.

---

## Features

- Normalize Myanmar text (remove unwanted spaces, support space removal modes)  
- Tokenize into syllables  
- Protection (FIXED ME: NW)
- Tokenize into words using grammar-rules
- Tokenize into words using (FIXED ME:) (forward/backward maximum matching + dictionary fallback)  
- Post-process: merge/split number tokens, split English words & punctuation  
- Optionally save tokenization results to CSV  

---

## Credit & Inspiration

This library draws inspiration from the [oppaWord: Myanmar Word Segmenter](https://github.com/ye-kyaw-thu/oppaWord) by Ye Kyaw Thu / LU Lab, especially in the approach to word segmentation using maximum matching (forward/backward), space removal modes (`my_not_num`, etc.), and dictionary-based lookup. The license of oppaWord is MIT.  

---
## Folder Structure
```
MMDT-TOKENIZER/
├─ pyproject.toml
├─ src/
│  └─ mmdt_tokenizer/
│     ├─ __init__.py
│     ├─ tokenizer/            
│     │  ├─ __init__.py
│     │  └─ core.py              ← defines MyanmarTokenizer
|     |  └─ syllable_tokenizer.py ← syllabus-based tokenizer
|     |  └─ word_tokenizer.py ← word-based tokenizer
|     |  └─ rule_segementer.py ← rule-based segmenter for word tokenization
│     ├─ utils/
│     │  ├─ __init__.py
│     │  ├─ constants.py
│     │  ├─ patterns.py
│     │  ├─ matching.py
│     │  ├─ chunking.py
│     │  └─ token_ops.py
│     ├─ preprocessing/
│     ├─ postprocessing/
│     ├─ data/
│     ├─ result/
│     └─ tests/
├─ .venv/                         
└─ README.md

```
---

## Installation

```bash
pip install mmdt-tokenizer
```
---
## License
Distributed under the MIT License. See LICENSE for more information.

---
## Changelog / Versioning

v0.1.0 — initial release with core tokenization features
