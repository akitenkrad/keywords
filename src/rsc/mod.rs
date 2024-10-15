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

impl Keywords {
    pub fn add(&mut self, keyword: Keyword) {
        self.keywords.push(keyword);
    }
    pub fn remove(&mut self, keyword: Keyword) {
        let index = self.keywords.iter().position(|x| x == &keyword).unwrap();
        self.keywords.remove(index);
    }
    pub fn get(&self, index: usize) -> &Keyword {
        &self.keywords[index]
    }
}

pub fn load_keywords() -> Keywords {
    let mut keywords = Keywords {
        keywords: Vec::new(),
    };
    keywords.keywords = serde_json::from_slice(SRC_JSON).expect("Unable to parse json");
    return keywords;
}
