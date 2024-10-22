use crate::mecab::mecab_tokenize;
use crate::SRC_JSON;
use regex::Regex;
use serde::{Deserialize, Serialize};
use serde_json;

#[cfg(test)]
mod tests;

#[derive(PartialEq, Debug, Serialize, Deserialize, Clone)]
pub enum Language {
    English,
    Japanese,
}

#[derive(PartialEq, Debug, Serialize, Deserialize, Clone)]
pub enum Category {
    MachineLearning,
    NaturalLanguageProcessing,
    Security,
    Organization,
    ComputerVision,
    Item,
    Topic,
    Task,
    Other,
}

#[derive(PartialEq, Debug, Serialize, Deserialize, Clone)]
pub struct Keyword {
    pub word: String,
    pub alias: String,
    pub score: u8,
    pub language: Language,
    pub category: Category,
}

#[derive(Debug)]
pub struct Keywords {
    pub keywords: Vec<Keyword>,
}

impl Keyword {
    pub fn get_keyword_ptn(&self) -> Regex {
        // _keyword = self.word.lower().replace("-", r"(\-|\s)*").replace(" ", r"(\s|\-)*")
        // return re.compile(
        //     rf"""(?P<PREK>(^|\s|\(|'|")+)(?P<KEYWORD>{_keyword}(s|ing|al|d|ed|\-[^\s]+)*)(?P<POSTK>($|\s|\.|,|:|;|\)|'|")+)""",
        //     flags=re.IGNORECASE | re.MULTILINE | re.DOTALL,
        let kwd = self
            .word
            .to_lowercase()
            .replace("-", r"(\-|\s)*")
            .replace(" ", r"(\s|\-)*");
        let ptn = format!(
            r#"(^|\s|\(|'|"|\-)+(?i){}(s|ing|al|d|ed|\-[^\s]+)*($|\s|\)|\(|\.|,|:|;|\)|'|")+"#,
            kwd
        );
        return Regex::new(&ptn).unwrap();
    }
}

pub fn load_keywords() -> Vec<Keyword> {
    return serde_json::from_slice(SRC_JSON).expect("Unable to parse json");
}

pub fn extract_keywords(text: &str, keywords: &Vec<Keyword>, lang: Language) -> Vec<Keyword> {
    let mut extracted_keywords: Vec<Keyword> = Vec::new();

    if lang == Language::English {
        for keyword in keywords {
            let re = keyword.get_keyword_ptn();
            if re.is_match(text) {
                extracted_keywords.push(keyword.clone());
            }
        }
    } else if lang == Language::Japanese {
        let tokens = mecab_tokenize(text);
        let text = tokens
            .iter()
            .map(|t| t.surface.clone())
            .collect::<Vec<String>>()
            .join(" ");
        for keyword in keywords {
            let re = keyword.get_keyword_ptn();
            if re.is_match(&text) {
                extracted_keywords.push(keyword.clone());
            }
        }
    }

    return extracted_keywords;
}
