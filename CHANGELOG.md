# Changelog

## [Unreleased]

### Added
- Implemented `MarketList` model using `MarketInformation` from auto-generated code
- Added `AccountList` model for handling user accounts
- Implemented error handling and logging in API functions

### Changed
- Updated `get_all_markets` function to return `List[MarketInformation]`
- Modified `RequestsExecutor` to use HTTP instead of HTTPS
- Updated test cases to use new models and error handling

### Fixed
- Resolved import issues with `MarketList` and `AccountList`
- Fixed SSL-related errors by switching to HTTP

## TODO
- [ ] Implement proper error handling for all API functions
- [ ] Add more comprehensive unit tests for all API functions
- [ ] Implement rate limiting for API requests
- [ ] Add documentation for all classes and functions
- [ ] Implement caching mechanism for frequently used data (e.g., market list)
- [ ] Add support for websocket connections for real-time data
- [ ] Implement retry mechanism for failed API requests
- [ ] Add type hints to all functions and classes
- [ ] Implement proper logging throughout the library
- [ ] Create examples and usage documentation

## [0.1.0] - 2024-10-22
### Added
- Initial version of the HaasLib API wrapper
- Basic functionality for authentication, market data retrieval, and account information
