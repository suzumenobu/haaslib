use core::fmt;

pub mod api;
pub mod domain;
pub mod lab;
pub mod model;

#[derive(Debug)]
pub enum Error {
    Failure(String),
    Lab(String),
    Http(String),
    Serde(String),
}

pub type Result<T> = std::result::Result<T, Error>;

impl From<reqwest::Error> for crate::Error {
    fn from(value: reqwest::Error) -> Self {
        Error::Http(value.to_string())
    }
}

impl From<serde_json::Error> for crate::Error {
    fn from(value: serde_json::Error) -> Self {
        Error::Serde(value.to_string())
    }
}

impl fmt::Display for crate::Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.to_string())
    }
}
