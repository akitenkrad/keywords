use super::*;
use std::time;

#[test]
fn test_sample() {
    let path = std::path::Path::new(".");
    println!("{:?}", path.display());
    // let mut f = csv::Reader::from_reader(std::io::Cursor::new(MECAB_USER_DIC));
    // let lines = f
    //     .records()
    //     .map(|r| r.unwrap())
    //     .collect::<Vec<csv::StringRecord>>();
    // println!("{:?}", lines[0].get(0));
}
#[test]
fn test_mecab_tokenize() {
    let tokens = mecab_tokenize("すもももももももものうち");
    assert!(tokens.len() > 0);

    let st = time::Instant::now();
    let tokens = mecab_tokenize("今日は晴れです。");
    assert!(tokens.len() > 0);
    println!("Elapsed: {:?}", st.elapsed());
}
