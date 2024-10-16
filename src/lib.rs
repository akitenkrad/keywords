pub mod mecab;
pub mod rsc;

const SRC_JSON: &'static [u8] = include_bytes!("rsc/rsc.json");
const MECAB_DIC: &'static str = "unidic-cwj-3_1_1+compact-dual/system.dic.zst";
const MECAB_USER_DIC: &'static str = include_str!("mecab/dic/user_dic.csv");
