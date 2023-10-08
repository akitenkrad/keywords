# keywords

## Get Started

### install
```bash
pip install git+ssh://git@github.com/akitenkrad/keywords.git
```

- get keywords

    ```python
    from keywords.keywords import Keyword
    keywords: list[Keyword] = Keyword.load_keywords()
    ```

- calculate metrics
    - specialization factor
        ```python
        from keywords.metrics import SpecializationFactor
        factors = SpecializationFactor.calculate(texts)
        ```
