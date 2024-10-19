from haaslib.api import RequestsExecutor, Authenticated, Guest
from haaslib.api import (
    get_all_labs,
    delete_lab,
    get_accounts,
    get_all_markets,
    get_all_markets_by_pricesource,
    get_lab_details,
    get_all_bots,
    delete_bot,
    add_bot,
    create_lab,
    HaasApiError,
)
from haaslib.model import CreateLabRequest, StartLabExecutionRequest, CloudMarket, MarketTag, CreateBotRequest, AddBotFromLabRequest
from loguru import logger
import time

class SimpleExecutor:
    def __init__(self, host, port, email, password):
        self.executor = RequestsExecutor(host=host, port=port, state=Guest())
        self.email = email
        self.password = password

    def authenticate(self):
        try:
            self.executor = self.executor.authenticate(email=self.email, password=self.password)
            logger.info("Successfully authenticated.")
        except HaasApiError as e:
            logger.error(f"Authentication failed: {e}")
            raise

    def get_all_labs(self):
        try:
            return get_all_labs(self.executor)
        except HaasApiError as e:
            logger.error(f"Error getting labs: {e}")
            raise

    def delete_lab(self, lab_id):
        try:
            return delete_lab(self.executor, lab_id)
        except HaasApiError as e:
            logger.error(f"Error deleting lab {lab_id}: {e}")
            raise

    def get_accounts(self):
        try:
            return get_accounts(self.executor)
        except HaasApiError as e:
            logger.error(f"Error getting accounts: {e}")
            raise

    def get_all_markets(self):
        try:
            return get_all_markets(self.executor)
        except HaasApiError as e:
            logger.error(f"Error getting markets: {e}")
            raise

    def get_all_markets_by_pricesource(self, price_source):
        try:
            return get_all_markets_by_pricesource(self.executor, price_source)
        except HaasApiError as e:
            logger.error(f"Error getting markets for price source {price_source}: {e}")
            raise

    def get_lab_details(self, lab_id):
        try:
            return get_lab_details(self.executor, lab_id)
        except HaasApiError as e:
            logger.error(f"Error getting lab details for {lab_id}: {e}")
            raise

    def get_all_bots(self):
        try:
            return get_all_bots(self.executor)
        except HaasApiError as e:
            logger.error(f"Error getting bots: {e}")
            raise

    def delete_bot(self, bot_id):
        try:
            return delete_bot(self.executor, bot_id)
        except HaasApiError as e:
            logger.error(f"Error deleting bot {bot_id}: {e}")
            raise

    def add_bot(self, req: CreateBotRequest):
        try:
            return add_bot(self.executor, req)
        except HaasApiError as e:
            logger.error(f"Error adding bot: {e}")
            raise

    def create_lab(self, req: CreateLabRequest):
        try:
            return create_lab(self.executor, req)
        except HaasApiError as e:
            logger.error(f"Error creating lab: {e}")
            raise
