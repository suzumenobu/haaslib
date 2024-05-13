/// Custom wrapper for backtest periods in UNIX time
#[derive(Clone, Copy, Debug)]
pub enum BacktestPeriod {
    Day(u64),
    Month(u64),
}

impl BacktestPeriod {
    pub fn as_secs(&self) -> u64 {
        match self {
            BacktestPeriod::Day(count) => 86400 * count,
            BacktestPeriod::Month(count) => 86400 * (*count as f64 * 30.5) as u64,
        }
    }

    pub fn as_days(&self) -> u64 {
        match self {
            BacktestPeriod::Day(count) => *count,
            BacktestPeriod::Month(count) => (*count as f64 * 30.5) as u64,
        }
    }
}

pub struct MarketTag(String);
