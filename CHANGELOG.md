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

### Added
- Implemented `get_random_account` function to retrieve a random user account
- Implemented `get_random_script` function to retrieve a random available script
- Implemented `get_random_market` function to retrieve a random available market
- Added `get_random_configuration` utility function to set up a random configuration including account, script, and market
- Incorporated automatically generated dataclasses from `Phyton_automatically_generated`:
  - `HaasBot`: Represents a Haas trading bot
  - `UserLabDetails`: Represents details of a user's lab

### Changed
- Updated `api_functions.py` to include new random selection functions
- Updated `model.py` to use the new automatically generated classes
- Modified `ScriptInfo`, `BotConfig`, and `LabConfig` classes to align with the new data structures
- Kept `MarketInfo` and `ApiResponse` classes as they contain useful additional information

### Changed
- Updated `model.py` to use the new automatically generated classes
- Modified `ScriptInfo`, `BotConfig`, and `LabConfig` classes to align with the new data structures
- Kept `MarketInfo` and `ApiResponse` classes as they contain useful additional information

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
- [ ] Resolve remaining import issues, particularly with MarketList and MarketInformation
- [ ] Implement remaining API functions from the Haas.com API documentation
- [ ] Add validation for API responses
- [ ] Implement proper exception handling and custom exceptions
- [ ] Add async versions of API functions for better performance
- [ ] Implement a command-line interface (CLI) for basic API interactions
- [ ] Add configuration file support for API credentials and other settings
- [ ] Implement a simple caching mechanism to reduce API calls for frequently accessed data
- [ ] Add support for different environments (development, staging, production)
- [ ] Implement proper session management for API calls
- [ ] Add support for pagination in API responses where applicable
- [ ] Implement proper logging throughout the library with different log levels
- [ ] Add support for API versioning
- [ ] Create a comprehensive README.md with installation and usage instructions
- [ ] Set up continuous integration (CI) for automated testing
- [ ] Implement proper error messages and debugging information
- [ ] Add support for different output formats (JSON, CSV, etc.)
- [ ] Implement a simple rate limiting mechanism to prevent API abuse
- [ ] Add support for bulk operations where applicable
- [ ] Implement proper data validation before sending requests to the API
- [ ] Add support for API key rotation and management
- [ ] Implement a simple plugin system for extending functionality
- [ ] Create a changelog generator script to automate changelog updates
- [ ] Implement error handling for cases where no accounts, scripts, or markets are available
- [ ] Add unit tests for new random selection functions
- [ ] Update documentation to include usage examples of new functions
- [ ] Consider adding parameters to random selection functions to allow filtering (e.g., by account type, script type, market attributes)
- [ ] Review and update all API functions to use the new data structures
- [ ] Update type hints throughout the codebase to use the new classes
- [ ] Add any missing fields or methods to the new classes as needed
- [ ] Update documentation to reflect the new class structures
- [ ] Add unit tests for the new and updated classes
- [ ] Ensure all serialization and deserialization methods work correctly with the new structures
- [ ] Review and update any functions that create or modify bot or lab configurations

## [0.1.0] - 2024-10-22
### Added
- Initial version of the HaasLib API wrapper
- Basic functionality for authentication, market data retrieval, and account information

