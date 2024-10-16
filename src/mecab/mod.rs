use crate::MECAB_DIC_PATH;
use crate::MECAB_USER_DIC;
use once_cell::sync::Lazy;
use std::fs;
use std::io::{BufReader, Cursor, Write};
use std::sync::Mutex;
use vibrato::tokenizer::worker::Worker;
use vibrato::{Dictionary, Tokenizer};

#[cfg(test)]
mod tests;

#[derive(Debug, Clone)]
pub struct MeCabToken {
    pub surface: String,
    pub pos1: String,
    pub pos2: String,
    pub feature: String,
}

static MECAB_TOKENIZER: Lazy<Tokenizer> = Lazy::new(|| get_tokenizer());
static MECAB_WORKER: Lazy<Mutex<Worker>> = Lazy::new(|| Mutex::new(MECAB_TOKENIZER.new_worker()));

fn get_tokenizer() -> Tokenizer {
    // create tokenizer
    let reader = zstd::Decoder::new(BufReader::new(MECAB_DIC_PATH)).unwrap();
    let mut dic = Dictionary::read(reader).unwrap();
    let mut f = csv::Reader::from_reader(Cursor::new(MECAB_USER_DIC));
    let lines = f
        .records()
        .map(|r| r.unwrap())
        .collect::<Vec<csv::StringRecord>>();
    if lines.len() > 0 {
        dic = dic
            .reset_user_lexicon_from_reader(Some(BufReader::new(Cursor::new(MECAB_USER_DIC))))
            .unwrap();
    }
    return Tokenizer::new(dic)
        .ignore_space(true)
        .unwrap()
        .max_grouping_len(24);
}

pub fn mecab_tokenize(text: &str) -> Vec<MeCabToken> {
    let mut tokens: Vec<MeCabToken> = Vec::new();
    MECAB_WORKER.lock().unwrap().reset_sentence(text);
    MECAB_WORKER.lock().unwrap().tokenize();

    for t in MECAB_WORKER.lock().unwrap().token_iter() {
        let features = t.feature().split(',').collect::<Vec<&str>>();
        tokens.push(MeCabToken {
            surface: t.surface().to_string(),
            pos1: features.get(0).unwrap_or(&"").to_string(),
            pos2: features.get(1).unwrap_or(&"").to_string(),
            feature: features.get(2).unwrap_or(&"").to_string(),
        });
    }
    return tokens;
}

pub fn add_word_to_user_dic(word: &str) {
    let mut f = csv::Reader::from_reader(std::io::Cursor::new(MECAB_USER_DIC));
    let lines = f
        .records()
        .map(|r| r.unwrap())
        .collect::<Vec<csv::StringRecord>>();
    let tokens = lines
        .iter()
        .map(|r| r.get(0).unwrap())
        .collect::<Vec<&str>>();

    if tokens.contains(&word) {
        return;
    }
    let mut file = fs::OpenOptions::new()
        .create(true)
        .append(true)
        .open("src/mecab/dic/user_dic.csv")
        .unwrap();
    file.write_all(format!("{},1000,1000,0,カスタム名詞,{}\n", word, word).as_bytes())
        .unwrap();
}
