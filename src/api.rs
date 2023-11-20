use crate::model::{self, CustomReport, PaginatedResponse, UserLabBacktestResult, UserLabDetails};
use crate::Result;
use anyhow::anyhow;
use log;
use reqwest::blocking::Client;
use serde::de::DeserializeOwned;

pub struct Api {
    address: String,
    port: String,
    protocol: String,
    client: Client,
    credentials: Option<UserCredentials>,
}

impl Api {
    pub fn new(address: String, port: String, protocol: String) -> Self {
        Self {
            address,
            port,
            protocol,
            client: Client::new(),
            credentials: None,
        }
    }

    pub fn app_login(&mut self, email: &str, secret_key: &str) -> Result<()> {
        let interface_key = (1..10)
            .map(|_| rand::random::<u8>().to_string())
            .collect::<String>();

        let uri = format!(
            "UserAPI.php?channel=APP_LOGIN&email={}&secretkey={}&interfaceKey={}",
            email, secret_key, interface_key
        );
        let resp = self.execute::<model::AppLogin, _>(uri, HttpMethod::Get)?;
        self.credentials = Some(UserCredentials {
            interface_key,
            user_id: resp.details.user_id,
        });

        Ok(())
    }

    pub fn all_markets(&self) -> Result<Vec<model::CloudMarket>> {
        let uri = "PriceAPI.php?channel=MARKETLIST";
        self.execute(uri, HttpMethod::Get)
    }

    pub fn markets(&self, price_source: &str) -> Result<Vec<model::CloudMarket>> {
        let uri = format!(
            "PriceAPI.php?channel=MARKETLIST&pricesource={}",
            price_source
        );
        self.execute(uri, HttpMethod::Get)
    }

    pub fn get_all_script_items(&self) -> Result<Vec<model::HaasScriptItemWithDependencies>> {
        let uri = self.wrap_with_credentials("HaasScriptAPI.php?channel=GET_ALL_SCRIPT_ITEMS")?;
        self.execute(uri, HttpMethod::Get)
    }

    pub fn get_accounts(&self) -> Result<Vec<model::UserAccount>> {
        let uri = self.wrap_with_credentials("AccountAPI.php?channel=GET_ACCOUNTS")?;
        self.execute(uri, HttpMethod::Get)
    }

    pub fn create_lab(&self, req: model::CreateLabRequest<'_>) -> Result<model::UserLabDetails> {
        let uri = self.wrap_with_credentials(format!(
            "LabsAPI.php?channel=CREATE_LAB&scriptId={}&name={}&accountId={}&market={}&interval={}&style={}",
            req.script_id, req.name, req.account_id, req.market, req.interval, req.style.value()
        ))?;
        self.execute(uri, HttpMethod::Get)
    }

    pub fn start_lab_execution(
        &self,
        req: model::StartLabExecutionRequest<'_>,
    ) -> Result<model::UserLabDetails> {
        let uri = self.wrap_with_credentials(format!(
            "LabsAPI.php?channel=START_LAB_EXECUTION&labid={}&startunix={}&endunix={}&sendemail={}",
            req.lab_id, req.start_unix, req.end_unix, req.send_email
        ))?;
        self.execute(uri, HttpMethod::Get)
    }

    pub fn get_lab_details(&self, lab_id: &str) -> Result<model::UserLabDetails> {
        let uri = self.wrap_with_credentials(format!(
            "LabsAPI.php?channel=GET_LAB_DETAILS&labid={}",
            lab_id
        ))?;
        self.execute(uri, HttpMethod::Get)
    }

    pub fn update_lab_details(&self, details: &UserLabDetails) -> Result<model::UserLabDetails> {
        let uri = self.wrap_with_credentials(format!(
            "LabsAPI.php?channel=UPDATE_LAB_DETAILS&labid={}&name={}&type={}&config={}&settings={}&parameters={}",
            details.lab_id,
            details.name,
            details.algorithm,
            urlencoding::encode(serde_json::to_string(&details.user_lab_config)?.as_str()),
            urlencoding::encode(serde_json::to_string(&details.haas_script_settings)?.as_str()),
            urlencoding::encode(serde_json::to_string(&details.parameters)?.as_str())
        ))?;
        self.execute(uri, HttpMethod::Get)
    }

    pub fn update_multiple_lab_details<'a>(
        &self,
        details: impl IntoIterator<Item = &'a UserLabDetails>,
    ) -> Result<Vec<model::UserLabDetails>> {
        details
            .into_iter()
            .map(|d| self.update_lab_details(d))
            .collect()
    }

    pub fn get_backtest_result<T>(
        &self,
        lab_id: &str,
        next_page_id: u64,
        page_length: u32,
    ) -> Result<PaginatedResponse<UserLabBacktestResult<T>>>
    where
        T: CustomReport + DeserializeOwned,
    {
        let url = self.wrap_with_credentials(format!(
            "LabsAPI.php?channel=GET_BACKTEST_RESULT_PAGE&labid={}&nextpageid={}&pagelength={}",
            lab_id, next_page_id, page_length
        ))?;
        self.execute(url, HttpMethod::Get)
    }

    fn execute<T, U>(&self, uri: U, method: HttpMethod) -> Result<T>
    where
        T: serde::de::DeserializeOwned,
        U: AsRef<str> + std::fmt::Display,
    {
        let url = format!("{}://{}:{}/{}", self.protocol, self.address, self.port, uri);

        log::trace!("Executing [{}]", url);

        let resp = match method {
            HttpMethod::Get => self.client.get(url).send()?,
        };

        resp.json::<model::ApiResponse<T>>()
            .map(|r| r.data)
            .map_err(|e| anyhow::anyhow!(e))
    }

    fn wrap_with_credentials<U: AsRef<str> + std::fmt::Display>(&self, uri: U) -> Result<String> {
        match &self.credentials {
            Some(creds) => Ok(format!(
                "{}&userid={}&interfacekey={}",
                uri, creds.user_id, creds.interface_key
            )),
            None => Err(anyhow!(
                "You should use `Api::app_login` before calling private API methods"
            )),
        }
    }
}

struct UserCredentials {
    user_id: String,
    interface_key: String,
}

enum HttpMethod {
    Get,
}
