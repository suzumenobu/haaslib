pub mod api;
pub mod domain;
pub mod lab;
pub mod model;

pub type Result<T> = std::result::Result<T, anyhow::Error>;
