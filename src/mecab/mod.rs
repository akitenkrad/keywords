use once_cell::sync::Lazy;
use std::fs;
use std::io::Write;
use std::sync::Mutex;
use vibrato::tokenizer::worker::Worker;
use vibrato::{Dictionary, Tokenizer};
use xz2::read::XzDecoder;
#[cfg(test)]
mod tests;

#[derive(Debug, Clone)]
pub struct MeCabToken {
    pub surface: String,
    pub pos1: String,
    pub pos2: String,
    pub feature: String,
}

const DIC_DIR: &str = "/usr/local/lib/mecab/dic/";
const DIC_PATH: &str = "/usr/local/lib/mecab/dic/unidic-cwj-3_1_1+compact-dual/system.dic.zst";
const DIC_URL: &str =
"https://github.com/daac-tools/vibrato/releases/download/v0.5.0/unidic-cwj-3_1_1+compact-dual.tar.xz";
const USER_DIC: &str = "/usr/local/lib/mecab/dic/user_dic.csv";

static MECAB_TOKENIZER: Lazy<Tokenizer> = Lazy::new(|| get_tokenizer());
static MECAB_WORKER: Lazy<Mutex<Worker>> = Lazy::new(|| Mutex::new(MECAB_TOKENIZER.new_worker()));

pub async fn download_dict() {
    if !fs::exists(DIC_DIR).unwrap() {
        fs::create_dir_all(DIC_DIR).unwrap();
    }
    if !fs::exists(DIC_PATH).unwrap() {
        let res = reqwest::get(DIC_URL).await.unwrap();
        let body = res.bytes().await.unwrap();
        let tar = XzDecoder::new(body.as_ref());
        let mut archive = tar::Archive::new(tar);
        archive.unpack(DIC_DIR).unwrap();
    }
}

fn get_tokenizer() -> Tokenizer {
    // create tokenizer
    let reader = zstd::Decoder::new(fs::File::open(DIC_PATH).unwrap()).unwrap();
    let mut dic = Dictionary::read(reader).unwrap();
    if fs::exists(USER_DIC).unwrap() {
        let lines = fs::read_to_string(USER_DIC).unwrap();
        if lines.len() > 0 {
            dic = dic
                .reset_user_lexicon_from_reader(Some(fs::File::open(USER_DIC).unwrap()))
                .unwrap();
        }
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
    let mut tokens: Vec<&str> = Vec::new();
    if fs::exists(USER_DIC).unwrap() {
        let user_dic_content = fs::read_to_string(USER_DIC).unwrap();
        for line in user_dic_content.lines() {
            let w = *line.split(',').collect::<Vec<&str>>().get(0).unwrap();
            tokens.push(w);
        }
        if tokens.contains(&word) {
            return;
        }
    }
    let mut file = fs::OpenOptions::new()
        .create(true)
        .append(true)
        .open(USER_DIC)
        .unwrap();
    file.write_all(format!("{},1000,1000,0,カスタム名詞,{}\n", word, word).as_bytes())
        .unwrap();
}
