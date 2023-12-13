use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::{
    collections::HashMap,
    time::{Duration, SystemTime, UNIX_EPOCH},
};
#[derive(Deserialize, Debug)] // Deserialize JSON into structure 
#[serde(rename_all = "PascalCase")] // Standardize naming convention on deserialization
pub struct ApiResponse<T> {

    pub success: bool,
    pub error: String,
    pub data: T,  
}

#[derive(Deserialize, Debug)]  
#[serde(rename_all = "PascalCase")]
pub struct AppLogin {

    pub is_success: bool, 
    pub error: i64,
    pub details: UserDetails,  
}

#[derive(Deserialize, Debug)]   
#[serde(rename_all = "PascalCase")] 
pub struct UserDetails {

    pub user_id: String,
    pub interface_secret: String, 
    pub license_details: serde_json::Value,
}

// Bot definition
#[derive(Default, Debug, Clone, PartialEq, Serialize, Deserialize)]  
pub struct HaasBot {
    
    // Field mappings to JSON  
    #[serde(rename = "UI")]
    pub user_id: String,
    #[serde(rename = "ID")]
    pub bot_id: String,
    #[serde(rename = "BN")]
    pub bot_name: String,
    #[serde(rename = "SI")]
    pub script_id: String,
    #[serde(rename = "SV")]
    pub script_version: i64,
    #[serde(rename = "AI")]
    pub account_id: String,
    #[serde(rename = "PM")]
    pub market: String,
    #[serde(rename = "EI")]
    pub execution_id: String,
    #[serde(rename = "IA")]
    pub is_activated: bool,
    #[serde(rename = "IP")]
    pub is_paused: bool,
    #[serde(rename = "IF")]
    pub is_favorite: bool,
    #[serde(rename = "NO")]
    pub notes: String,
    #[serde(rename = "SN")]
    pub script_note: String,
    #[serde(rename = "NT")]
    pub notes_timestamp: i64,
    #[serde(rename = "RP")]
    pub realized_profit: f64,
    #[serde(rename = "UP")]
    pub urealized_profit: f64,
    #[serde(rename = "ROI")]
    pub return_on_investment: f64,
    #[serde(rename = "TAE")]
    pub trade_amount_error: bool,
    #[serde(rename = "AE")]
    pub account_error: bool,
    #[serde(rename = "SE")]
    pub script_error: bool,
    #[serde(rename = "UC")]
    pub update_counter: i64,
    #[serde(rename = "CI")]
    pub chart_interval: i64,
    #[serde(rename = "CS")]
    pub chart_style: i64,
    #[serde(rename = "CV")]
    pub chart_volume: bool,
    #[serde(rename = "IWL")]
    pub is_white_label: bool,
    #[serde(rename = "MBID")]
    pub master_bot_id: String,
    #[serde(rename = "F")]
    pub followers: i64,
}
// Script item with dependencies
#[derive(Default, Debug, Clone, PartialEq, Deserialize)]
pub struct HaasScriptItemWithDependencies {
    #[serde(rename = "D")]
    pub dependencies: Vec<String>,
    #[serde(rename = "UID")]
    pub user_id: String,
    #[serde(rename = "SID")]
    pub script_id: String,
    #[serde(rename = "SN")]
    pub script_name: String,
    #[serde(rename = "SD")]
    pub script_description: String,
    #[serde(rename = "ST")]
    pub script_type: i64,
    #[serde(rename = "SS")]
    pub script_status: i64,
    #[serde(rename = "CN")]
    pub command_name: String,
    #[serde(rename = "IC")]
    pub is_command: bool,
    #[serde(rename = "IV")]
    pub is_valid: bool,
    #[serde(rename = "CU")]
    pub created_unix: i64,
    #[serde(rename = "UU")]
    pub updated_unix: i64,
    #[serde(rename = "FID")]
    pub folder_id: i64,
}
// Lab creation request 
#[derive(Clone)]
pub struct CreateLabRequest<'a> {
    pub script_id: &'a str,
    pub name: String,
    pub account_id: &'a str,
    pub market: &'a str,
    pub interval: u32,
    pub style: HaasChartPricePlotStyle,
}

#[derive(Clone, Copy)]
pub enum HaasChartPricePlotStyle {
    CandleStick,
}

impl HaasChartPricePlotStyle {
    pub fn value(&self) -> u32 {
        use HaasChartPricePlotStyle::*;

        match self {
            CandleStick => 300,
        }
    }
}
// User accounts 
#[derive(Default, Debug, Clone, PartialEq, Deserialize)]
pub struct UserAccount {
    #[serde(rename = "UID")]
    pub user_id: String,
    #[serde(rename = "AID")]
    pub account_id: String,
    #[serde(rename = "N")]
    pub name: String,
    #[serde(rename = "EC")]
    pub exchnage_code: String,
    #[serde(rename = "ET")]
    pub exchange_type: i64,
    #[serde(rename = "S")]
    pub status: i64,
    #[serde(rename = "IS")]
    pub is_simulated: bool,
    #[serde(rename = "IT")]
    pub is_test_net: bool,
    #[serde(rename = "PA")]
    pub is_public: bool,
    #[serde(rename = "WL")]
    pub is_white_label: bool,
    #[serde(rename = "PM")]
    pub position_mode: i64,
    #[serde(rename = "MS")]
    pub margin_settings: serde_json::Value,
    #[serde(rename = "V")]
    pub version: i64,
}
// Lab details
#[derive(Debug, PartialEq, Deserialize, Serialize)]
pub struct UserLabDetails {
    #[serde(rename = "C")]
    pub user_lab_config: UserLabConfig,
    #[serde(rename = "ST")]
    pub haas_script_settings: HaasScriptSettings,
    #[serde(rename = "P")]
    pub parameters: Vec<UserLabParameter>,
    #[serde(rename = "UID")]
    pub user_id: String,
    #[serde(rename = "LID")]
    pub lab_id: String,
    #[serde(rename = "SID")]
    pub script_id: String,
    #[serde(rename = "N")]
    pub name: String,
    #[serde(rename = "T")]
    pub algorithm: i64,
    #[serde(rename = "S")]
    pub status: UserLabStatus,
    #[serde(rename = "SB")]
    pub scheduled_backtests: i64,
    #[serde(rename = "CB")]
    pub complete_backtests: i64,
    #[serde(rename = "CA")]
    pub created_at: i64,
    #[serde(rename = "UA")]
    pub updated_at: i64,
    #[serde(rename = "SA")]
    pub started_at: i64,
    #[serde(rename = "RS")]
    pub running_since: i64,
    #[serde(rename = "SU")]
    pub start_unix: i64,
    #[serde(rename = "EU")]
    pub end_unix: i64,
    #[serde(rename = "SE")]
    pub send_email: bool,
    #[serde(rename = "CM")]
    pub cancel_reason: serde_json::Value,
}
// Lab status enum
#[derive(Debug, PartialEq, serde_repr::Serialize_repr, serde_repr::Deserialize_repr)]
#[repr(u8)]
pub enum UserLabStatus {
    Created = 0,
    Queued = 1,
    Running = 2,
    Completed = 3,
    Cancelled = 4,
}

#[derive(Default, Debug, Clone, PartialEq, Deserialize, Serialize)]
pub struct UserLabConfig {
    #[serde(rename = "MP")]
    pub max_population: i64,
    #[serde(rename = "MG")]
    pub max_generations: i64,
    #[serde(rename = "ME")]
    pub max_elites: i64,
    #[serde(rename = "MR")]
    pub mix_rate: f64,
    #[serde(rename = "AR")]
    pub adjust_rate: f64,
}

#[derive(Default, Debug, Clone, PartialEq, Deserialize, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct HaasScriptSettings {
    pub bot_id: String,
    pub bot_name: String,
    pub account_id: String,
    pub market_tag: String,
    pub position_mode: i64,
    pub margin_mode: i64,
    pub leverage: f64,
    pub trade_amount: f64,
    pub interval: i64,
    pub chart_style: i64,
    pub order_template: i64,
    pub script_parameters: ScriptParameters,
}

#[derive(Default, Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct ScriptParameters {}

#[derive(Default, Debug, Clone, PartialEq, Deserialize, Serialize)]
pub struct UserLabParameter {
    #[serde(rename = "K")]
    pub key: String,
    #[serde(rename = "T")]
    pub input_field_type: i64,
    #[serde(rename = "O")]
    pub options: Vec<UserLabParameterOption>,
    #[serde(rename = "I")]
    pub is_enabled: bool,
    #[serde(rename = "IS")]
    pub is_specific: bool,
}

#[derive(Deserialize, Serialize, Debug, Clone, PartialEq)]
#[serde(untagged)]
pub enum UserLabParameterOption {
    String(String),
    Digit(i64),
    Float(f64),
    Bool(bool),
}
// Structs for lab config, settings, parameters 

// Start lab execution  
pub struct StartLabExecutionRequest<'a> {
    pub lab_id: &'a str,
    pub start_unix: u64,
    pub end_unix: u64,
    pub send_email: bool,
}

impl<'a> StartLabExecutionRequest<'a> {
    pub fn new(lab_id: &'a str, period: BacktestPeriod, send_email: bool) -> Self {
        let end_unix = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap() // It's OK, UNIX_EPOCH always earlier then now
            .as_secs()
            - 100; // Some diff between real now cause API bug

        let start_unix = end_unix - Duration::from_secs(period.as_secs()).as_secs();
        Self {
            lab_id,
            send_email,
            start_unix,
            end_unix,
        }
    }
}
// Market from cloud provider 
#[derive(Default, Debug, Clone, PartialEq, Deserialize)]
pub struct CloudMarket {
    #[serde(rename = "PS")]
    pub price_source: String,
    #[serde(rename = "P")]
    pub primary: String,
    #[serde(rename = "S")]
    pub secondary: String,
}

impl std::fmt::Display for CloudMarket {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "{} {}/{}",
            self.price_source, self.primary, self.secondary
        )
    }
}

impl CloudMarket {
    pub fn as_market_tag(&self) -> String {
        format!("{}_{}_{}_", self.price_source, self.primary, self.secondary)
    }
}
// Backtest time periods
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
// Paginated responses
#[derive(Default, Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct PaginatedResponse<T> {
    #[serde(rename = "I")]
    pub items: Vec<T>,
    #[serde(rename = "NP")]
    pub next_page_id: i64,
}
// Backtest result 
#[derive(Default, Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct UserLabBacktestResult<T: CustomReport> {
    #[serde(rename = "RID")]
    pub record_id: i64,
    #[serde(rename = "UID")]
    pub user_id: String,
    #[serde(rename = "LID")]
    pub lab_id: String,
    #[serde(rename = "BID")]
    pub backtest_id: String,
    #[serde(rename = "NG")]
    pub generation_idx: i64,
    #[serde(rename = "NP")]
    pub population_idx: i64,
    #[serde(rename = "ST")]
    pub status: i64,
    #[serde(rename = "SE")]
    pub settings: HaasScriptSettings,
    #[serde(rename = "P")]
    pub parameters: HashMap<String, String>,
    #[serde(rename = "RT")]
    pub runtime: Value,
    #[serde(rename = "C")]
    pub chart: Value,
    #[serde(rename = "L")]
    pub logs: Value,
    #[serde(rename = "S")]
    pub summary: UserLabsBacktestSummary<T>,
}

#[derive(Default, Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct UserLabsBacktestSummary<T: CustomReport> {
    #[serde(rename = "O")]
    pub o: i64,
    #[serde(rename = "T")]
    pub t: i64,
    #[serde(rename = "P")]
    pub p: i64,
    #[serde(rename = "FC")]
    pub fc: HashMap<String, f32>,
    #[serde(rename = "RP")]
    pub rp: HashMap<String, f32>,
    #[serde(rename = "ROI")]
    pub roi: Vec<f64>,
    #[serde(rename = "CR")]
    pub custom_report: CustomReportWrapper<T>,
}

#[derive(Debug, Clone, PartialEq, Deserialize, Default, Serialize)]
pub struct CustomReportWrapper<T> {
    #[serde(rename = "Custom Report")]
    pub data: T,
}
// Trait for custom reports 
pub trait CustomReport: PartialEq + Clone {}

#[cfg(test)]
mod tests {
    use serde_json::json;

    use crate::model::UserLabParameterOption;

    #[test]
    fn desers_lab_parameters() {
        let json = json!([1, "2"]);
        let actual: Vec<UserLabParameterOption> = serde_json::from_str(&json.to_string()).unwrap();
        assert_eq!(
            actual,
            vec![
                UserLabParameterOption::Digit(1),
                UserLabParameterOption::String("2".to_string())
            ]
        );
    }
}
