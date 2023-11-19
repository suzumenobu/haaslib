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

pub fn update_params<'a, S: ToString + 'a>(
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

pub fn execute<T>(
    api: &Api,
    lab_id: &str,
    period: BacktestPeriod,
) -> Result<PaginatedResponse<UserLabBacktestResult<T>>>
where
    T: CustomReport + DeserializeOwned,
{
    let req = StartLabExecutionRequest::new(lab_id, period, false);
    api.start_lab_execution(req)?;
    lab::wait_for_lab_execution(api, lab_id)?;
    api.get_backtest_result(lab_id, 0, 1_000_000)
}

pub fn wait_for_lab_execution(api: &Api, lab_id: &str) -> Result<()> {
    loop {
        match api.get_lab_details(lab_id)?.status {
            UserLabStatus::Completed => {
                log::info!("Execution completed!");
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
