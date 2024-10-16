pub mod mecab;
pub mod rsc;

const SRC_JSON: &'static [u8] = include_bytes!("rsc/rsc.json");
const MECAB_DIC_PATH: &'static [u8] = include_bytes!("mecab/dic/system.dic.zst");
const MECAB_USER_DIC: &'static str = include_str!("mecab/dic/user_dic.csv");
