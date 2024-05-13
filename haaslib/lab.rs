/// Module providing utility functions for managing HaasScript parameters and executing labs.
///
/// # Examples
///
/// ## Creating a ChangeHaasScriptParameterRequest
/// ```
/// use crate::lab_execution::{ChangeHaasScriptParameterRequest, UserLabParameterOption};
///
/// let request = ChangeHaasScriptParameterRequest::new("ParameterName", vec![UserLabParameterOption::Digit(42)]);
/// ```
///
/// ## Updating HaasScript Parameters
/// ```
/// use crate::lab_execution::{ChangeHaasScriptParameterRequest, update_params, UserLabParameter, UserLabParameterOption};
///
/// let mut parameters: Vec<UserLabParameter> = //... get current parameters
/// let request = ChangeHaasScriptParameterRequest::new("ParameterName", vec![UserLabParameterOption::Digit(42)]);
///
/// update_params(&mut parameters, &[&request])?;
/// ```
///
/// ## Executing a Lab and Waiting for Execution to Complete
/// ```
/// use crate::lab_execution::{execute, wait_for_lab_execution};
/// use crate::api::{Authenticated, ReqwestExecutor};
/// use crate::model::BacktestPeriod;
/// use crate::Result;
///
/// fn execute_lab(executor: &ReqwestExecutor<Authenticated>, lab_id: &str) -> Result<()> {
///     let period = BacktestPeriod::Day;
///     execute(executor, lab_id, period)?;
///     wait_for_lab_execution(executor, lab_id)?;
///     Ok(())
/// }
/// ```
use crate::{
    api::{self, Authenticated, Executor},
    domain::BacktestPeriod,
    lab,
    model::{
        CustomReport, PaginatedResponse, StartLabExecutionRequest, UserLabBacktestResult,
        UserLabParameter, UserLabParameterOption, UserLabStatus,
    },
    Error, Result,
};
use serde::de::DeserializeOwned;

impl From<UserLabParameterOption> for String {
    fn from(val: UserLabParameterOption) -> Self {
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

/// Struct representing a request to change a HaasScript parameter.
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

/// Updates HaasScript parameters based on a collection of ChangeHaasScriptParameterRequest.
///
/// # Arguments
///
/// * `settings` - The current HaasScript parameters to be updated.
/// * `params` - An iterator over ChangeHaasScriptParameterRequest containing the updates.
///
/// # Returns
///
/// A Result indicating success or an error if the update fails.
pub fn update_params<'a, S: ToString + 'a>(
    settings: &mut [UserLabParameter],
    params: impl IntoIterator<Item = &'a ChangeHaasScriptParameterRequest<S>>,
) -> Result<()> {
    for param in params.into_iter() {
        let param_name = param.name.to_string().to_lowercase();

        let setting = settings
            .iter_mut()
            .find(|s| s.key.to_lowercase().contains(&param_name))
            .ok_or(Error::Lab(format!(
                "Failed to find {} in setting",
                param.name.to_string()
            )))?;

        setting.options = param.options.clone()
    }
    Ok(())
}

/// Executes a lab and retrieves the backtest result for an authenticated user.
///
/// # Arguments
///
/// * `executor` - The API executor for an authenticated user.
/// * `lab_id` - The ID of the lab to execute.
/// * `period` - The backtest period to use.
///
/// # Returns
///
/// A Result containing a PaginatedResponse with UserLabBacktestResult items if successful,
/// or an error if the API call fails.
pub fn execute<T>(
    executor: &impl Executor<Authenticated>,
    lab_id: &str,
    period: BacktestPeriod,
) -> Result<PaginatedResponse<UserLabBacktestResult<T>>>
where
    T: CustomReport + DeserializeOwned,
{
    let req = StartLabExecutionRequest::new(lab_id, period, false);

    api::start_lab_execution(executor, req)?;

    lab::wait_for_lab_execution(executor, lab_id)?;

    api::get_backtest_result(executor, lab_id, 0, 1_000_000)
}

/// Waits for the execution of a lab to complete.
///
/// # Arguments
///
/// * `executor` - The API executor for an authenticated user.
/// * `lab_id` - The ID of the lab to monitor.
///
/// # Returns
///
/// A Result indicating success or an error if the lab execution fails.
pub fn wait_for_lab_execution(executor: &impl Executor<Authenticated>, lab_id: &str) -> Result<()> {
    loop {
        let details = api::get_lab_details(executor, lab_id)?;
        match details.status {
            UserLabStatus::Completed => {
                log::debug!("Execution of {} completed!", details.name);
                break;
            }
            UserLabStatus::Cancelled => {
                log::warn!("Lab {} was canceled", lab_id);

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
