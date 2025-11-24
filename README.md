## Grammar-based Text Segmentation

The mmdt-tokenizer is designed with a grammar-oriented approach to Myanmar text segmentation.
It models tokenization through the grammatical structure of the language, particularly the use of postpositions, particles, and predicate constructions.

### Core Principles

**Pattern Protection**

Before segmentation, special patterns such as URLs, numbers, emails, and date formats are temporarily protected to prevent accidental splitting during tokenization.

**Grammar-driven lexicons**

Lexicons are built around grammatical categories such as postpositions, conjunctions, sentence-final particles, auxiliary verbs, and negation markers.
Each entry is syllable-based, allowing flexible matching and better handling of morphological variations.

**Pipeline-based rule segmentation**

The tokenization process passes through a defined sequence of grammatical matchers (e.g., POSTP, AUX, SFP, NEG), which reflect the syntactic order of Myanmar sentences.

**Structural merging**

Rules like merge_predicate() combine related chunks (e.g., verb + auxiliary + negation + particle) into coherent grammatical units, producing more linguistically meaningful tokens.

**Extensible design**

The system is designed to grow with additional grammatical patterns and lexicon types without retraining, making it adaptable for both general text and domain-specific applications.

### Summary 

This approach enables ***mmdt-tokenizer*** to segment Myanmar text based on grammar and structure — resulting in context-aware tokenization that aligns with natural language syntax.

---

## Features

- Normalize Myanmar text (remove unwanted spaces, support space removal modes)  (Developed by NW)
- Tokenize into syllables  (Developed by NW)
- Protection (Developed by NW)
- Tokenize into words using grammar-rules (Developed by Myo)
- Optionally save tokenization results to CSV  (Developed by NW)

---

## Credit & Inspiration

This library draws inspiration from the [oppaWord: Myanmar Word Segmenter](https://github.com/ye-kyaw-thu/oppaWord) by Ye Kyaw Thu. The license of oppaWord is MIT.  

---

## Folder Structure
```
src/
└── mmdt_tokenizer/
    ├── __init__.py
    ├── core.py
    │
    ├── data/
    │
    ├── preprocessing/
    │   ├── __init__.py
    │   ├── cleaner.py
    │   ├── normalizer.py
    │   ├── preprocess.py
    │   └── protector.py
    │
    ├── rule_segmenter/
    │   ├── __init__.py
    |   ├── cleaner.py
    │   ├── collapse.py
    │   ├── engine.py
    │   ├── lexicon.py
    │   ├── merge_ops.py
    │   ├── scanner.py
    │   └── types.py
    │
    ├── tokenizer/
    │   ├── __init__.py
    │   ├── syllable_tokenizer.py
    │   └── word_tokenizer.py
    │
    ├── utils/
    │   ├── __init__.py
    │   ├── config.py
    │   ├── csv_utils.py
    │   ├── data_utils.py
    │   └── patterns.py
    │
    ├── scripts/
    │   ├── build_lexicons.py
    │   └── build_lexicons.ipynb
    │
    └── tests/
└─ pyproject.toml
└─ LICENSE    
└─ README.md

```
---
| Folder                | Purpose                                                                             |
| :-------------------- | :---------------------------------------------------------------------------------- |
| **`data/`**           | Holds raw and formatted datasets, lexicon CSVs, and output files.                   |
| **`preprocessing/`**  | Handles text cleaning, normalization, and input preparation.                        |
| **`rule_segmenter/`** | Core rule-based segmentation logic, including lexicon operations and chunk merging. |
| **`tokenizer/`**      | Contains syllable-level and word-level tokenizers.                                  |
| **`utils/`**          | Utility functions — CSV and data handling, text patterns, configs, and helpers.     |
| **`scripts/`**        | Developer utilities and notebooks (e.g., lexicon builder).                          |
| **`tests/`**          | Unit and integration test cases for validation.                                     |
| **`core.py`**         | Main entry module coordinating tokenization and pipeline components.                |

---

## Installation

```bash
pip install mmdt-tokenizer
```

## Usage Example

```bash
from mmdt_tokenizer import MyanmarTokenizer

tokenizer = MyanmarTokenizer()

text = "သူသွားမယ်သို့မဟုတ်သူလာမယ်။"
tokens = tokenizer.word_tokenize(text)

print(tokens)
# Expected Output: ["သူ", "သွားမယ်", "သို့မဟုတ်", "သူ", "လာမယ်။"]

```
---
## License
Distributed under the MIT License. See LICENSE for more information.

---
## Changelog / Versioning

v0.1.0 — initial release with core tokenization features
