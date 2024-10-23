ц # HaasLib

Client for [HaasOnline](https://www.haasonline.com) API. Allows automation of Haas trading infrastructure.

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
4. [API Coverage](#api-coverage)
5. [Contributing](#contributing)
6. [License](#license)

## Features

- Robust API Client handling communication with HaasOnline API
- Utilities to create, execute, and monitor backtests
- Type-safe classes for key entities like markets, accounts, and bots
- Custom result handling with Pydantic models
- Comprehensive error handling and logging

## Installation
bash
pip install haaslib


## Usage

First, create an `executor` which will interact with the API:
python
from haaslib import api
executor = api.RequestsExecutor(host="127.0.0.1", port=8090, state=api.Guest())

## Authenticate to access all endpoints:
python
executor = executor.authenticate(email="your_email@example.com", password="your_password")
