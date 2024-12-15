use pyo3::prelude::*;

pub mod mecab;
pub mod rsc;

const SRC_JSON: &'static [u8] = include_bytes!("rsc/rsc.json");
const MECAB_DIC: &'static str = "unidic-cwj-3_1_1+compact-dual/system.dic.zst";
const MECAB_USER_DIC: &'static str = include_str!("mecab/dic/user_dic.csv");

#[pymodule(name = "keywords")]
fn keywords(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<rsc::Language>()?;
    m.add_class::<rsc::Category>()?;
    m.add_class::<rsc::Keyword>()?;
    m.add_function(wrap_pyfunction!(rsc::load_keywords, m)?)?;
    m.add_function(wrap_pyfunction!(rsc::load_keywords_from_rsc, m)?)?;
    m.add_function(wrap_pyfunction!(rsc::extract_keywords, m)?)?;
    Ok(())
}
