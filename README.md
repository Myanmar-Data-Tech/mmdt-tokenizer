## mmdt-tokenizer
A Myanmar text tokenizer library (“mmdt-tokenizer”) for word- and syllable-level tokenization, normalization, and preprocessing. Useful for processing Burmese , mixed text, numbers, and English segments.

---

## Features

- Normalize Myanmar text (remove unwanted spaces, support space removal modes)  
- Tokenize into syllables  
- Tokenize into words using forward/backward maximum matching + dictionary fallback  
- Post-process: merge/split number tokens, split English words & punctuation  
- Optionally save tokenization results to CSV  

---

## Credit & Inspiration

This library draws inspiration from the [oppaWord: Myanmar Word Segmenter](https://github.com/ye-kyaw-thu/oppaWord) by Ye Kyaw Thu / LU Lab, especially in the approach to word segmentation using maximum matching (forward/backward), space removal modes (`my_not_num`, etc.), and dictionary-based lookup. The license of oppaWord is MIT.  

---
## Folder Structure

- `LICENSE` — license file (MIT)  
- `pyproject.toml` — project metadata & build config  
- `src/mmdt_tokenizer/` — the main library package  
  - `constants.py` — regexes, unicode letter/digit classes etc.  
  - `preprocess.py` — text cleanup, space removal  
  - `segment.py` — word segmentation logic (forward/backward matching)  
  - `postprocess.py` — refining tokens (number merging, splitting, English)  
  - `csv_utils.py` — save token outputs to CSV  
  - `word_tokenizer.py` — word-level tokenizer class  
  - `syllable_tokenizer.py` — syllable-level tokenizer class  
  - `core.py` — facade class `MyanmarTokenizer` that wraps the above  
- `tests/` — unit tests  

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
