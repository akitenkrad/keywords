use crate::MECAB_DIC;
use crate::MECAB_USER_DIC;
use indicatif::ProgressBar;
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

const DIC_URL: &str = "https://github.com/daac-tools/vibrato/releases/download/v0.5.0/unidic-cwj-3_1_1+compact-dual.tar.xz";
fn download_dic() {
    let rt = tokio::runtime::Builder::new_current_thread()
        .enable_all()
        .build()
        .unwrap();
    rt.block_on(async {
        let response = reqwest::get(DIC_URL).await;
        let body = response.unwrap().bytes().await.unwrap();
        let decoder = xz2::read::XzDecoder::new(&body[..]);
        let mut archive = tar::Archive::new(decoder);
        let dic_dir = format!("{}/.mecab/dic/", std::env::var("HOME").unwrap());
        if !fs::exists(dic_dir.as_str()).unwrap() {
            fs::create_dir_all(dic_dir.as_str()).unwrap();
        }
        archive.unpack(dic_dir.as_str()).unwrap();
    })
}

async fn download_dic_async() {
    let response = reqwest::get(DIC_URL).await;
    let body = response.unwrap().bytes().await.unwrap();
    let decoder = xz2::read::XzDecoder::new(&body[..]);
    let mut archive = tar::Archive::new(decoder);
    let dic_dir = format!("{}/.mecab/dic/", std::env::var("HOME").unwrap());
    if !fs::exists(dic_dir.as_str()).unwrap() {
        fs::create_dir_all(dic_dir.as_str()).unwrap();
    }
    archive.unpack(dic_dir.as_str()).unwrap();
}

fn get_tokenizer() -> Tokenizer {
    // create tokenizer
    let mecab_dic_path = format!(
        "{}/.mecab/dic/{}",
        std::env::var("HOME").unwrap(),
        MECAB_DIC
    );
    if !fs::exists(mecab_dic_path.as_str()).unwrap() {
        if tokio::runtime::Handle::try_current().is_ok() {
            tokio::runtime::Handle::try_current()
                .unwrap()
                .spawn(async { download_dic_async().await });
        } else {
            download_dic();
        }
    }

    // wait until the dictionary is downloaded
    loop {
        let bar = ProgressBar::new(300);
        let mut retry_count = 300;
        if fs::exists(mecab_dic_path.as_str()).unwrap() {
            break;
        }
        std::thread::sleep(std::time::Duration::from_secs(1));
        retry_count -= 1;
        bar.inc(1);

        if retry_count == 0 {
            panic!("Failed to download MeCab dictionary");
        }
    }

    let reader = zstd::Decoder::new(fs::File::open(mecab_dic_path).unwrap()).unwrap();
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
