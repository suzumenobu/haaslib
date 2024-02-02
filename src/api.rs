/// Module providing an API client for interacting with a remote service using the Reqwest library.
/// The client supports both guest and authenticated users and includes methods for various API calls.
///
/// # Examples
///
/// ## Creating a Guest User Executor
/// ```
/// use crate::api_client::{ReqwestExecutor, GuestUser};
///
/// let executor = ReqwestExecutor::new("example.com", "8080", "https");
/// ```
///
/// ## Authenticating and Creating an Authenticated User Executor
/// ```
/// use crate::api_client::{ReqwestExecutor, GuestUser};
///
/// let executor = ReqwestExecutor::new("example.com", "8080", "https")
///     .authenticate("user@example.com", "secret_key")
///     .expect("Authentication failed");
/// ```
///
/// ## Making API Calls
/// ```
/// use crate::api_client::{ReqwestExecutor, AuthenticatedUser, HttpMethod, all_markets};
///
/// let executor = ReqwestExecutor::new("example.com", "8080", "https")
///     .authenticate("user@example.com", "secret_key")
///     .expect("Authentication failed");
///
/// let markets = all_markets(&executor);
/// ```
///
/// ## Updating HaasScript Parameters
/// ```rust
/// use crate::model::{ChangeHaasScriptParameterRequest, update_params, UserLabParameter, UserLabParameterOption};
///
/// let mut parameters: Vec<UserLabParameter> = //... get current parameters
/// let request = ChangeHaasScriptParameterRequest::new("ParameterName", vec![UserLabParameterOption::Digit(42)]);
///
/// update_params(&mut parameters, &[&request]).unwrap();
/// ```
/// ## Creating and Executing Labs
/// ```rust
/// use crate::model::{CreateLabRequest, HaasChartPricePlotStyle, BacktestPeriod};
/// use crate::api::{Authenticated, ReqwestExecutor};
/// use crate::lab_execution::{execute, wait_for_lab_execution};
/// use crate::Result;
///
/// fn create_and_execute_lab(executor: &ReqwestExecutor<Authenticated>) -> Result<()> {
///     let lab_request = CreateLabRequest {
///         script_id: "script123",
///         name: String::from("MyLab"),
///         account_id: "account123",
///         market: "BTC/USD",
///         interval: 5,
///         style: HaasChartPricePlotStyle::CandleStick,
///     };
///
///     let lab_id = api::create_lab(executor, lab_request)?;
///
///     let period = BacktestPeriod::Day(1);
///     execute(executor, &lab_id, period)?;
///     wait_for_lab_execution(executor, &lab_id)?;
///
///     Ok(())
/// }
/// ```
use crate::model::{
    self, AppLogin, CustomReport, EditHaasScriptSourceCodeSettings, PaginatedResponse,
    UserLabBacktestResult, UserLabDetails,
};
use crate::Result;
use log;
use reqwest::blocking::Client;
use serde::de::DeserializeOwned;

/// Struct representing user credentials for authentication.
struct UserCredentials {
    /// Returned from the server
    user_id: String,
    /// Generated on the client side
    interface_key: String,
}

/// Guest client marker type.
pub struct Guest;

/// Authenticated client marker type.
pub struct Authenticated {
    credentials: UserCredentials,
}

/// Interface for intercating with HTTP server
pub trait Executor<S> {
    /// Executes an API call with the specified URI.
    ///
    /// # Arguments
    ///
    /// * `uri` - The URI for the API endpoint.
    ///
    /// # Returns
    ///
    /// A Result containing the deserialized response data if successful,
    /// or an error if the API call fails.
    ///
    /// # Generic Parameters
    ///
    /// * `T` - The type to deserialize the API response into.
    /// * `U` - The type of the URI, typically a string or a reference to a string.
    fn execute<T, U>(&self, uri: U) -> Result<T>
    where
        T: serde::de::DeserializeOwned,
        U: AsRef<str> + std::fmt::Display;
}

/// Actual impl of `Executor` with reqwest crate
pub struct ReqwestExecutor<S> {
    client: Client,
    address: String,
    port: String,
    protocol: String,
    state: S,
}

impl ReqwestExecutor<Guest> {
    pub fn new(address: impl ToString, port: impl ToString, protocol: impl ToString) -> Self {
        Self {
            client: Client::new(),
            state: Guest,
            address: address.to_string(),
            port: port.to_string(),
            protocol: protocol.to_string(),
        }
    }

    /// Authenticates the guest client and returns an executor for authenticated client.
    pub fn authenticate(
        self,
        email: &str,
        secret_key: &str,
    ) -> Result<ReqwestExecutor<Authenticated>> {
        let interface_key = (1..10)
            .map(|_| rand::random::<u8>().to_string())
            .collect::<String>();

        let uri = format!(
            "UserAPI.php?channel=LOGIN_WITH_CREDENTIALS&email={}&password={}&interfaceKey={}",
            email, secret_key, interface_key
        );

        let resp = self.execute::<model::ApiResponse<serde_json::Value>, _>(uri)?;
        log::debug!("Resp: {resp:?}");

        let uri = format!(
            "UserAPI.php?channel=LOGIN_WITH_ONE_TIME_CODE&email={}&pincode=000000&interfaceKey={}",
            email, interface_key
        );
        let resp = self.execute::<model::ApiResponse<Option<AppLogin>>, _>(uri)?;
        log::debug!("Resp: {resp:?}");

        let credentials = UserCredentials {
            interface_key,
            user_id: resp
                .data
                .expect("Failed to authenticate. Check your credentials in the config")
                .details
                .user_id,
        };

        Ok(ReqwestExecutor {
            state: Authenticated { credentials },
            client: self.client,
            address: self.address,
            port: self.port,
            protocol: self.protocol,
        })
    }
}

impl Executor<Guest> for ReqwestExecutor<Guest> {
    fn execute<T, U>(&self, uri: U) -> crate::Result<T>
    where
        T: serde::de::DeserializeOwned,
        U: AsRef<str> + std::fmt::Display,
    {
        let url = format!("{}://{}:{}/{}", self.protocol, self.address, self.port, uri);

        log::trace!("Executing [{}]", url);

        let resp = self.client.get(url).send()?;

        log::trace!("Got {:?} resp", resp.status());

        let text = resp.text()?;
        log::trace!("{}", &text);

        Ok(serde_json::from_str(&text)?)
    }
}

impl ReqwestExecutor<Authenticated> {
    fn wrap_with_credentials<U: AsRef<str> + std::fmt::Display>(&self, uri: U) -> String {
        format!(
            "{}&userid={}&interfacekey={}",
            uri, self.state.credentials.user_id, self.state.credentials.interface_key
        )
    }
}
impl Executor<Authenticated> for ReqwestExecutor<Authenticated> {
    fn execute<T, U>(&self, uri: U) -> crate::Result<T>
    where
        T: serde::de::DeserializeOwned,
        U: AsRef<str> + std::fmt::Display,
    {
        let url = format!("{}://{}:{}/{}", self.protocol, self.address, self.port, uri);

        let url = self.wrap_with_credentials(url);

        let resp = self.client.get(url).send()?;

        Ok(resp.json::<model::ApiResponse<T>>().map(|r| r.data)?)
    }
}
// region:     --- API functions

/// Retrieves information about all available markets.
///
/// # Arguments
///
/// * `executor` - The API executor to use for making the API call.
///
/// # Returns
///
/// A Result containing a vector of CloudMarket if successful, or an error if the API call fails.
pub fn get_all_markets<S>(executor: &impl Executor<S>) -> Result<Vec<model::CloudMarket>> {
    let uri = "PriceAPI.php?channel=MARKETLIST";
    executor.execute(uri)
}

/// Retrieves information about markets from a specific price source.
///
/// # Arguments
///
/// * `executor` - The API executor to use for making the API call.
/// * `price_source` - The specific price source for which market information is requested.
///
/// # Returns
///
/// A Result containing a vector of CloudMarket if successful, or an error if the API call fails.
pub fn get_all_markets_by_pricesource<S>(
    executor: &impl Executor<S>,
    price_source: &str,
) -> Result<Vec<model::CloudMarket>> {
    let uri = format!(
        "PriceAPI.php?channel=MARKETLIST&pricesource={}",
        price_source
    );
    executor.execute(uri)
}

/// Retrieves information about all script items for an authenticated user.
///
/// # Arguments
///
/// * `executor` - The API executor for an authenticated user.
///
/// # Returns
///
/// A Result containing a vector of HaasScriptItemWithDependencies if successful,
/// or an error if the API call fails.
pub fn get_all_script_items(
    executor: &impl Executor<Authenticated>,
) -> Result<Vec<model::HaasScriptItemWithDependencies>> {
    executor.execute("HaasScriptAPI.php?channel=GET_ALL_SCRIPT_ITEMS")
}

/// Retrieves information about user accounts for an authenticated user.
///
/// # Arguments
///
/// * `executor` - The API executor for an authenticated user.
///
/// # Returns
///
/// A Result containing a vector of UserAccount if successful, or an error if the API call fails.
pub fn get_accounts(executor: &impl Executor<Authenticated>) -> Result<Vec<model::UserAccount>> {
    executor.execute("AccountAPI.php?channel=GET_ACCOUNTS")
}

/// Creates a new lab for an authenticated user.
///
/// # Arguments
///
/// * `executor` - The API executor for an authenticated user.
/// * `req` - The CreateLabRequest containing details for creating the lab.
///
/// # Returns
///
/// A Result containing UserLabDetails if successful, or an error if the API call fails.
pub fn create_lab(
    executor: &impl Executor<Authenticated>,
    req: model::CreateLabRequest,
) -> Result<model::UserLabDetails> {
    let uri = format!(
            "LabsAPI.php?channel=CREATE_LAB&scriptId={}&name={}&accountId={}&market={}&interval={}&style={}",
            req.script_id, req.name, req.account_id, req.market, req.interval, req.style.value()
        );
    executor.execute(uri)
}

/// Starts the execution of a lab for an authenticated user.
///
/// # Arguments
///
/// * `executor` - The API executor for an authenticated user.
/// * `req` - The StartLabExecutionRequest containing details for starting the lab execution.
///
/// # Returns
///
/// A Result containing UserLabDetails if successful, or an error if the API call fails.
pub fn start_lab_execution(
    executor: &impl Executor<Authenticated>,
    req: model::StartLabExecutionRequest<'_>,
) -> Result<model::UserLabDetails> {
    let uri = format!(
        "LabsAPI.php?channel=START_LAB_EXECUTION&labid={}&startunix={}&endunix={}&sendemail={}",
        req.lab_id, req.start_unix, req.end_unix, req.send_email
    );
    executor.execute(uri)
}

/// Retrieves details about a specific lab for an authenticated user.
///
/// # Arguments
///
/// * `executor` - The API executor for an authenticated user.
/// * `lab_id` - The ID of the lab for which details are requested.
///
/// # Returns
///
/// A Result containing UserLabDetails if successful, or an error if the API call fails.
pub fn get_lab_details(
    executor: &impl Executor<Authenticated>,
    lab_id: &str,
) -> Result<model::UserLabDetails> {
    let uri = format!("LabsAPI.php?channel=GET_LAB_DETAILS&labid={}", lab_id);
    executor.execute(uri)
}

/// Updates details for a specific lab for an authenticated user.
///
/// # Arguments
///
/// * `executor` - The API executor for an authenticated user.
/// * `details` - The updated UserLabDetails for the lab.
///
/// # Returns
///
/// A Result containing UserLabDetails if successful, or an error if the API call fails.
pub fn update_lab_details(
    executor: &impl Executor<Authenticated>,
    details: &UserLabDetails,
) -> Result<model::UserLabDetails> {
    let uri = format!(
            "LabsAPI.php?channel=UPDATE_LAB_DETAILS&labid={}&name={}&type={}&config={}&settings={}&parameters={}",
            details.lab_id,
            details.name,
            details.algorithm,
            urlencoding::encode(serde_json::to_string(&details.user_lab_config)?.as_str()),
            urlencoding::encode(serde_json::to_string(&details.haas_script_settings)?.as_str()),
            urlencoding::encode(serde_json::to_string(&details.parameters)?.as_str())
        );
    executor.execute(uri)
}

/// Updates details for multiple labs for an authenticated user.
///
/// # Arguments
///
/// * `executor` - The API executor for an authenticated user.
/// * `details` - An iterator over UserLabDetails representing the labs to be updated.
///
/// # Returns
///
/// A Result containing a vector of updated UserLabDetails if successful,
/// or an error if any API call fails.
pub fn update_multiple_lab_details<'a>(
    executor: &impl Executor<Authenticated>,
    details: impl IntoIterator<Item = &'a UserLabDetails>,
) -> Result<Vec<model::UserLabDetails>> {
    details
        .into_iter()
        .map(|d| update_lab_details(executor, d))
        .collect()
}

/// Retrieves the backtest result for a specific lab for an authenticated user.
///
/// # Arguments
///
/// * `executor` - The API executor for an authenticated user.
/// * `lab_id` - The ID of the lab for which the backtest result is requested.
/// * `next_page_id` - The ID of the next page for paginated results.
/// * `page_length` - The number of items per page for paginated results.
///
/// # Returns
///
/// A Result containing a PaginatedResponse with UserLabBacktestResult items if successful,
/// or an error if the API call fails.
pub fn get_backtest_result<T>(
    executor: &impl Executor<Authenticated>,
    lab_id: &str,
    next_page_id: u64,
    page_length: u32,
) -> Result<PaginatedResponse<UserLabBacktestResult<T>>>
where
    T: CustomReport + DeserializeOwned,
{
    let url = format!(
        "LabsAPI.php?channel=GET_BACKTEST_RESULT_PAGE&labid={}&nextpageid={}&pagelength={}",
        lab_id, next_page_id, page_length
    );
    executor.execute(url)
}

pub fn edit_haas_script_source_code<T>(
    executor: &impl Executor<Authenticated>,
    script_id: &str,
    sourcecode: &str,
    settings: EditHaasScriptSourceCodeSettings,
) -> Result<()> {
    let url = format!(
        "HaasScriptAPI.php?channel=EDIT_SCRIPT_SOURCECODE&scriptid={}&sourcecode={}&settings={}",
        script_id,
        urlencoding::encode(serde_json::to_string(&sourcecode)?.as_str()),
        urlencoding::encode(serde_json::to_string(&settings)?.as_str()),
    );
    executor.execute(url)
}

// endregion:  --- API functions
