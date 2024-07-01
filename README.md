# keywords

## Get Started

### install
```bash
pip install git+ssh://git@github.com/akitenkrad/keywords.git
```

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
