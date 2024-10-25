from typing import Optional
from .executor import RequestsExecutor, Guest, Authenticated
from .managers.lab_manager import LabManager
from .managers.market_manager import MarketManager
from .managers.account_manager import AccountManager
from .exceptions import AuthenticationError
from .config import Settings, config

class HaasClient:
    """High-level client for HaasOnline Trading Server API"""
    
    def __init__(
        self,
        settings: Optional[Settings] = None,
        executor: Optional[RequestsExecutor] = None
    ):
        self.settings = settings or config
        self.executor = executor or RequestsExecutor(
            host=self.settings.API_HOST,
            port=self.settings.API_PORT,
            state=Guest(),
            protocol=self.settings.API_PROTOCOL
        )
        
        # Initialize managers
        self.markets = MarketManager(self.executor)
        self._lab_manager: Optional[LabManager] = None
        self._account_manager: Optional[AccountManager] = None

    def authenticate(
        self,
        email: Optional[str] = None,
        password: Optional[str] = None
    ) -> 'HaasClient':
        """Authenticate with the API"""
        email = email or self.settings.API_EMAIL
        password = password or self.settings.API_PASSWORD
        
        if not email or not password:
            raise AuthenticationError(
                "Email and password must be provided either in settings or as parameters"
            )
        
        self.executor = self.executor.authenticate(email=email, password=password)
        
        # Initialize authenticated managers
        self._lab_manager = LabManager(self.executor)
        self._account_manager = AccountManager(self.executor)
        
        return self

    @property
    def lab(self) -> LabManager:
        """Get lab manager, ensuring authentication"""
        if not self._lab_manager:
            raise AuthenticationError("Authentication required for lab operations")
        return self._lab_manager

    @property
    def accounts(self) -> AccountManager:
        """Get account manager, ensuring authentication"""
        if not self._account_manager:
            raise AuthenticationError("Authentication required for account operations")
        return self._account_manager
