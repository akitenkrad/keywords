[![CircleCI](https://dl.circleci.com/status-badge/img/circleci/X1fiE4koKU88Z9sKwWoPAH/D8z2Q2gapEqvFmMEfhA7cE/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/circleci/X1fiE4koKU88Z9sKwWoPAH/D8z2Q2gapEqvFmMEfhA7cE/tree/main)

# keywords

<img src="../LOGO.png" alt="LOGO" width=150, height=150 />

## Get Started

### for Rust

#### Installation

```bash
cargo add keyword-tools
```

#### Usage

```rust
use keyword_tools::{extract_keywords, load_keywords, load_keywords_from_rsc, Language};
let keywords = load_keywords();
// keywords = load_keywords_from_rsc(PATH_TO_JSON_FILE);
let text = "After the introduction of Large Language Models (LLMs), there have been substantial improvements in the performance of Natural Language Generation (NLG) tasks, including Text Summarization and Machine Translation.";

let extracted_kwds = extract_keywords(text, Language::English);
```

### for Python

#### Installation

```bash
pip install git+ssh://git@github.com/akitenkrad/keywords.git
```

#### Usage

- get keywords

    ```python
    from keywords import Keyword
    keywords: list[Keyword] = Keyword.load_keywords()
    ```

- extract keywords from texts

    ```python
    from keywords import Keyword, extract_keywords
    keywords: list[Keyword] = Keyword.load_keywords()
    extracted_kws = extract_keywords(text, keywords, remove_stopwords=True)
    ```

- calculate metrics
  - specialization factor

    ```python
    from keywords.metrics import SpecializationFactor
    factors = SpecializationFactor.calculate(texts)
    ```

## Use your keywords

If you want to use your own keywords, just create your a JSON file according to the following instructions:

```json
[
  {
    "category": "Topic",
    "language": "English",
    "word": "Edge AI",
    "alias": "Edge AI",
    "score": 10
  },
]
```

Then, load the keywords.

```rust
let kws = load_keywords_from_rsc("PATH_TO_YOUR JSON_FILE")
```

The JSON file defines a collection of topic entries used by the crate. Each entry is an object with the following fields:

### category

Specifies the category of the entry.  
Available options:

- Topic
- Security
- ComputerVision
- Organization
- MachineLearning
- Item
- NaturalLanguageProcessing

### Language

Indicates the language of the entry.  
Available options:

- Japanese
- English

### word

The main term or keyword for the topic.

### alias

An alternative name or synonym for the word.

### score

A numerical value representing the importance or relevance of the topic.
Available options:
Any integer or floating-point number (e.g., 1, 10). Higher values may indicate greater importance.
