/// Contains helper functions for executing backtests 
/// Handles configuring, running, monitoring and collecting results

use crate::{
    api::Api,
    lab,
    model::{
        BacktestPeriod, CustomReport, PaginatedResponse, StartLabExecutionRequest,
        UserLabBacktestResult, UserLabParameter, UserLabParameterOption, UserLabStatus,
    },
    Result,
};
use anyhow::anyhow;
use serde::de::DeserializeOwned;
/// Helper to convert between option types
impl From<UserLabParameterOption> for String {
    fn from(val: UserLabParameterOption) -> Self {
        /// Match on inner type and convert 
        use UserLabParameterOption::*;
        match val {
            Digit(i) => i.to_string(),
            Float(f) => f.to_string(),
            Bool(b) => b.to_string(),
            String(s) => s,
        }
    }
}

impl From<i64> for UserLabParameterOption {
    fn from(val: i64) -> Self {
        UserLabParameterOption::Digit(val)
    }
}

impl From<f64> for UserLabParameterOption {
    fn from(val: f64) -> Self {
        UserLabParameterOption::Float(val)
    }
}

impl From<String> for UserLabParameterOption {
    fn from(val: String) -> Self {
        UserLabParameterOption::String(val)
    }
}

pub struct ChangeHaasScriptParameterRequest<T: ToString> {
    pub name: T,
    pub options: Vec<UserLabParameterOption>,
}

impl<S: ToString> ChangeHaasScriptParameterRequest<S> {
    pub fn new<T>(name: S, options: impl IntoIterator<Item = T>) -> Self
    where
        T: Into<UserLabParameterOption>,
    {
        ChangeHaasScriptParameterRequest {
            name,
            options: options
                .into_iter()
                .map(Into::<UserLabParameterOption>::into)
                .collect::<Vec<_>>(),
        }
    }
}
/// Similar helpers for other types

/// Handles configuring parameters before backtest run  
pub fn update_params<'a, S: ToString + 'a>(
    /// Finds param in settings by name
    /// Updates options value  
    settings: &mut [UserLabParameter],
    params: impl IntoIterator<Item = &'a ChangeHaasScriptParameterRequest<S>>,
) -> Result<()> {
    for param in params.into_iter() {
        let param_name = param.name.to_string().to_lowercase();

        let setting = settings
            .iter_mut()
            .find(|s| s.key.to_lowercase().contains(&param_name))
            .ok_or(anyhow!(
                "Failed to find {} in settings",
                param.name.to_string()
            ))?;

        setting.options = param.options.clone()
    }
    Ok(())
}
/// Kicks off backtest and collects result
pub fn execute<T>(
    api: &Api,
    lab_id: &str,
    period: BacktestPeriod,
) -> Result<PaginatedResponse<UserLabBacktestResult<T>>>
where
    T: CustomReport + DeserializeOwned,
{
    let req = StartLabExecutionRequest::new(lab_id, period, false);
    /// Starts execution
    api.start_lab_execution(req)?;
    /// Wait for status != Running
    lab::wait_for_lab_execution(api, lab_id)?;
     /// Fetch all pages of results 
    api.get_backtest_result(lab_id, 0, 1_000_000)
}
/// Polls status API till backtest finishes
pub fn wait_for_lab_execution(api: &Api, lab_id: &str) -> Result<()> {
    loop {
        let details = api.get_lab_details(lab_id)?;
        match details.status {
            UserLabStatus::Completed => {
                log::debug!("Execution of {} completed!", details.name);
                break;
            }
            UserLabStatus::Cancelled => {
                log::warn!("Lab {} was canceled", lab_id);
                /// Exit loop when done
                break;
            }
            status => {
                log::debug!("Got status: {:?}", status);
            }
        }

        std::thread::sleep(std::time::Duration::from_secs(5));
    }
    Ok(())
}
