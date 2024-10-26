use super::*;

#[test]
fn test_keywords_load() {
    let keywords = load_keywords();
    println!("{}", keywords.len());
    assert!(keywords.len() > 0);
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
    let re_str = keyword.get_keyword_ptn();
    let re = Regex::new(&re_str).unwrap();
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

#[test]
fn test_extract_keywords_english() {
    let text = "This is a Transformer model.";
    let keywords = load_keywords();
    let extracted_keywords = extract_keywords(text, keywords, Language::English);
    println!("{:?}", extracted_keywords);
    assert!(extracted_keywords.len() > 0);
}

#[test]
fn test_extract_keywords_japanese() {
    let text = "これはTransformerモデルです。";
    let keywords = load_keywords();
    let extracted_keywords = extract_keywords(text, keywords, Language::Japanese);
    println!("{:?}", extracted_keywords);
    assert!(extracted_keywords.len() > 0);
}

#[test]
fn test_each_keywords() {
    let kws = load_keywords();
    for kw in kws.into_iter() {
        let surface = kw.word.clone();
        let text_en = format!("This is {} .", surface);
        let text_ja = format!("これは{}です。", surface);
        let extracted_keywords_en = extract_keywords(&text_en, vec![kw.clone()], Language::English);
        let extracted_keywords_ja =
            extract_keywords(&text_ja, vec![kw.clone()], Language::Japanese);

        if !extracted_keywords_en.contains(&kw) {
            println!(
                "WARNING!(EN): {:?} (extracted: {:?})",
                kw, extracted_keywords_en
            );
        }
        if !extracted_keywords_ja.contains(&kw) {
            println!(
                "WARNING!(JA): {:?} (extracted: {:?})",
                kw, extracted_keywords_ja
            );
        }
    }
}
