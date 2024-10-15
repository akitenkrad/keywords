use super::*;

#[test]
fn test_keywords_load() {
    let keywords = load_keywords();
    println!("{}", keywords.keywords.len());
    assert!(keywords.keywords.len() > 0);
}

#[test]
fn test_keyword_get_keyword_ptn() {
    let keyword = Keyword {
        word: "Transformer".to_string(),
        alias: "ML".to_string(),
        score: 10,
        language: Language::English,
        category: Category::MachineLearning,
    };
    let re = keyword.get_keyword_ptn();
    assert!(re.is_match("Transformer"));
    assert!(re.is_match("transformer"));
    assert!(re.is_match("transformers"));
    assert!(re.is_match("transformer-like"));
    assert!(re.is_match("super-transformer"));
    assert!(re.is_match("transformer's"));
    assert!(re.is_match("transformer."));
    assert!(re.is_match("transformer,"));
    assert!(re.is_match("transformer:"));
    assert!(re.is_match("transformer;"));
    assert!(re.is_match("transformer)"));
    assert!(re.is_match("transformer'"));
    assert!(re.is_match("transformer\""));
    assert!(re.is_match("transformer("));
    assert!(re.is_match("this is a transformer."));
}
