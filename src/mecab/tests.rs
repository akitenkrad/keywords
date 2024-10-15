use super::*;
use std::fs;
use std::time;

#[test]
fn test_download_dict() {
    tokio_test::block_on(download_dict());
    assert!(fs::exists(DIC_DIR).unwrap());
    assert!(fs::exists(DIC_PATH).unwrap());
}

#[test]
fn test_mecab_tokenize() {
    tokio_test::block_on(download_dict());
    let tokens = mecab_tokenize("すもももももももものうち");
    assert_eq!(tokens.len(), 7);
    assert_eq!(tokens[0].surface, "すもも");
    assert_eq!(tokens[0].pos1, "名詞");
    assert_eq!(tokens[0].pos2, "普通名詞");

    let st = time::Instant::now();
    let tokens = mecab_tokenize("今日は晴れです。");
    assert_eq!(tokens.len(), 5);
    assert_eq!(tokens[0].surface, "今日");
    assert_eq!(tokens[0].pos1, "名詞");
    assert_eq!(tokens[0].pos2, "普通名詞");
    println!("Elapsed: {:?}", st.elapsed());
}

#[test]
fn test_add_word_to_user_dic() {
    tokio_test::block_on(download_dict());
    add_word_to_user_dic("斎藤飛鳥");
    add_word_to_user_dic("ビットコイン");
    add_word_to_user_dic("サムアルトマン");

    let tokens =
        mecab_tokenize("東京都斎藤飛鳥本とカレーの街やビットコインとサムアルトマン ChatGPT");
    println!("{:?}", tokens);
    assert_eq!(tokens.len(), 14);
}
