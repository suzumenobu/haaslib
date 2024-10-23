"""Test configuration and fixtures"""
import os
from typing import Generator
import pytest
from dotenv import load_dotenv

from haaslib import RequestsExecutor, Guest, Authenticated
from haaslib.config import Config

@pytest.fixture(scope="session")
def config() -> Config:
    """Load test configuration"""
    load_dotenv()
    return Config()

@pytest.fixture
def guest_executor(config: Config) -> RequestsExecutor[Guest]:
    """Create guest executor"""
    return RequestsExecutor(
        host=config.API_HOST,
        port=config.API_PORT,
        state=Guest(),
        protocol=config.API_PROTOCOL
    )

@pytest.fixture
def authenticated_executor(
    guest_executor: RequestsExecutor[Guest],
    config: Config
) -> Generator[RequestsExecutor[Authenticated], None, None]:
    """Create authenticated executor"""
    executor = guest_executor.authenticate(
        email=config.API_EMAIL,
        password=config.API_PASSWORD
    )
    yield executor
