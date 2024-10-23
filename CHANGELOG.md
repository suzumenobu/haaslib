# Changelog

## [Unreleased]

### Added
- Implemented new `RequestsExecutor` class in `executor.py` for improved API interaction
- Created `ApiResponse` generic class to handle various response types
- Added new custom exception classes: `HaasApiError`, `AuthenticationError`
- Implemented enhanced authentication flow in `RequestsExecutor`
- Added `Guest` and `Authenticated` state classes for better user authentication handling
- Created `get_all_markets_by_pricesource` function in `executor.py`
- Implemented comprehensive unit tests in `test_api_v2.py` covering API accessibility, authentication, and various API operations
- Added `config.py` using Pydantic for robust configuration management
- Created `logging_config.py` for centralized logging setup
- Implemented all placeholder functions in `api_functions.py` with full functionality

### Changed
- Refactored `RequestsExecutor` to use a more modular and type-safe approach
- Updated `model.py` to use both custom and auto-generated Pydantic models for improved data validation
- Modified `RequestsExecutor` to use HTTP instead of HTTPS by default, with configurable protocol
- Updated import statements across multiple files for better organization and clarity
- Refactored `test_api_v2.py` to use unittest framework with mock objects for comprehensive testing
- Updated `ApiResponse` to allow arbitrary types and use Pydantic's `ConfigDict` for enhanced flexibility
- Improved error handling throughout the library with more specific exception types
- Updated documentation in `ARCHITECTURE.md` to reflect the new structure and components

### Fixed
- Resolved issues with Pydantic schema generation for `ApiResponse`
- Fixed authentication flow to properly handle multi-step authentication process
- Improved market list retrieval functionality for better performance and error handling

### Removed
- Deprecated old API calling methods in favor of the new `RequestsExecutor` approach

### Security
- Enhanced authentication process with better error handling and security checks

## [0.1.0] - 2024-10-22
### Added
- Initial version of the HaasLib API wrapper
- Basic functionality for authentication, market data retrieval, and account information
