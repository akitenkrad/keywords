use crate::mecab::mecab_tokenize;
use crate::SRC_JSON;
use pyo3::prelude::*;
use regex::Regex;
use serde::{Deserialize, Serialize};
use serde_json;
use std::hash::Hasher;

#[cfg(test)]
mod tests;

#[pyclass(eq, eq_int)]
#[derive(PartialEq, Debug, Serialize, Deserialize, Clone)]
pub enum Language {
    English,
    Japanese,
}

#[pyclass(eq, eq_int)]
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

#[pyclass]
#[derive(PartialEq, Debug, Serialize, Deserialize, Clone)]
pub struct Keyword {
    pub word: String,
    pub alias: String,
    pub score: isize,
    pub language: Language,
    pub category: Category,
}

#[pymethods]
impl Keyword {
    pub fn get_keyword_ptn(&self) -> String {
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
        return ptn;
    }

    fn __repr__(slf: &Bound<'_, Self>) -> PyResult<String> {
        Ok(format!(
            "Keyword(word={}, alias={}, score={}, language={:?}, category={:?})",
            slf.borrow().word,
            slf.borrow().alias,
            slf.borrow().score,
            slf.borrow().language,
            slf.borrow().category
        ))
    }

    fn __str__(&self) -> String {
        return format!(
            "Keyword(word={}, alias={}, score={}, language={:?}, category={:?})",
            self.word, self.alias, self.score, self.language, self.category
        );
    }
    fn __hash__(&self) -> u64 {
        let mut hasher = std::collections::hash_map::DefaultHasher::new();
        hasher.write(&self.word.as_bytes());
        hasher.write(&self.alias.as_bytes());
        hasher.write_isize(self.score);
        return hasher.finish();
    }
    fn word(&self) -> String {
        return self.word.clone();
    }
    fn alias(&self) -> String {
        return self.alias.clone();
    }
    fn score(&self) -> isize {
        return self.score;
    }
    fn language(&self) -> String {
        return format!("{:?}", self.language);
    }
    fn category(&self) -> String {
        return format!("{:?}", self.category);
    }
}

#[pyfunction]
pub fn load_keywords() -> Vec<Keyword> {
    return serde_json::from_slice(SRC_JSON).expect("Unable to parse json");
}

#[pyfunction]
pub fn extract_keywords(text: &str, keywords: Vec<Keyword>, lang: Language) -> Vec<Keyword> {
    let mut extracted_keywords: Vec<Keyword> = Vec::new();

    if lang == Language::English {
        for keyword in keywords {
            let re_str = keyword.get_keyword_ptn();
            let re = Regex::new(&re_str).unwrap();
            if re.is_match(text) {
                extracted_keywords.push(keyword.clone());
            }
        }
    } else if lang == Language::Japanese {
        let tokens = mecab_tokenize(text);
        let mecabed_text = tokens
            .iter()
            .map(|t| t.surface.clone())
            .collect::<Vec<String>>()
            .join(" ");
        for keyword in keywords {
            let re_str = keyword.get_keyword_ptn();
            let re = Regex::new(&re_str).unwrap();
            if text.contains(&keyword.word) {
                extracted_keywords.push(keyword.clone());
            } else if re.is_match(&mecabed_text) {
                extracted_keywords.push(keyword.clone());
            }
        }
    }

    return extracted_keywords;
}
