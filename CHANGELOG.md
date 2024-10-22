# Changelog

## [Unreleased]

### Modified Files
- haaslib/__init__.py
  - Updated import statements
  - Added error handling for imports

- haaslib/api.py
  - Updated import statements
  - Modified RequestsExecutor to use HTTP instead of HTTPS

- haaslib/domain.py
  - [Add a brief description of changes made to this file]

- haaslib/executor.py
  - [Add a brief description of changes made to this file]

- haaslib/model.py
  - Added MarketList model using MarketInformation from auto-generated code
  - Updated CloudMarket model
  - Added AccountList and UserAccount models

- haaslib/test_api_v2.py
  - Updated import statements
  - Modified test cases to use new models and error handling

### New Files
- haaslib/api_functions.py
  - Implemented get_all_markets and get_accounts functions
  - Added error handling and logging

- haaslib/config.py
  - Added configuration settings for API host, port, and credentials

- haaslib/logging_config.py
  - Implemented logging configuration

### Untracked Files
- haaslib.log
  - [Note: This is likely a log file generated during testing. Consider adding it to .gitignore]

## TODO
- [ ] Review and update all API functions for consistency with new models
- [ ] Implement proper error handling for all API functions
- [ ] Add more comprehensive unit tests for all API functions
- [ ] Verify and update all import statements across the project
- [ ] Implement rate limiting for API requests
- [ ] Add documentation for all classes and functions
- [ ] Implement caching mechanism for frequently used data (e.g., market list)
- [ ] Add support for websocket connections for real-time data
- [ ] Implement retry mechanism for failed API requests
- [ ] Add type hints to all functions and classes
- [ ] Create examples and usage documentation

## [0.1.0] - 2024-10-22
### Added
- Initial version of the HaasLib API wrapper
- Basic functionality for authentication, market data retrieval, and account information
