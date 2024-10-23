# HaasLib Architecture

## Overview
HaasLib is a Python wrapper for the Haas API, providing an easy-to-use interface for interacting with Haas trading services. The library is designed with a focus on type safety, modularity, and ease of use.

## Key Components

### 1. RequestsExecutor (executor.py)
- Main class for making API calls
- Handles authentication and maintains session state
- Supports both authenticated and guest requests
- Uses generic typing for better type safety

#### Authentication Flow
1. Create a Guest RequestsExecutor
2. Call the `authenticate` method with credentials
3. Receive an Authenticated RequestsExecutor
4. Use the Authenticated RequestsExecutor for subsequent API calls

### 2. API Functions (api_functions.py)
- Contains high-level functions for interacting with the Haas API
- Each function corresponds to a specific API endpoint
- Utilizes the RequestsExecutor for making API calls
- Provides a clean interface for users of the library

### 3. API Response Structure

The API response structure has two layers: the outer structure handled by the `ApiResponse` class, and the inner structure of the `Data` field.

#### Outer Structure (ApiResponse class)
python 
{
class ApiResponse(Generic[ApiResponseData]):
Success: bool
Error: Optional[str] = None
Data: Optional[ApiResponseData] = None
}

#### Inner Structure (Data field)
The `Data` field typically contains the following structure:
python
{
'R': int, # Result Code
'D': Any, # Main Data Payload
'DID': str # Document/Data ID (possibly for request tracking)
}


The `ApiResponseData` type in the outer structure is flexible and can accommodate various types of data, including the inner structure shown above. This design allows for backward compatibility with existing API responses while providing a more type-safe and flexible wrapper for future extensions.

When working with API responses:
1. First, the response is parsed into the `ApiResponse` structure.
2. If `Success` is True, the `Data` field will contain the actual response data.
3. The contents of the `Data` field can then be further processed based on the specific API call, often mapping the 'D' key to a specific Pydantic model for that endpoint.

### 4. State Classes (executor.py)
- `Guest`: Represents unauthenticated state
- `Authenticated`: Represents authenticated state, contains UserId and InterfaceKey

### 5. Model Definitions (model.py)
- Uses Pydantic for data validation and serialization
- Combines custom and auto-generated models

### 6. Configuration (config.py)
- Manages API configuration settings (host, port, credentials)

### 7. Logging (logging_config.py)
- Configures logging for the library

### 8. Custom Exceptions
- `HaasApiError`: Custom exception for API-related errors

## Key Concepts

### UserId
- Critical for authenticated requests
- May be returned in either LOGIN_WITH_CREDENTIALS or LOGIN_WITH_ONE_TIME_CODE step
- Stored in Authenticated state and included in all authenticated requests

### InterfaceKey
- Generated for each authentication attempt
- Used in authentication process and subsequent requests

### DID (Document/Data ID)
- Unique identifier returned in API responses
- May be used for request tracking or correlation

## API Endpoints
- User: Authentication and user-related operations
- Account: Account information and management
- Price: Market and pricing data
- Bot: Trading bot operations
- HaasScript: Script management
- Labs: (Purpose to be determined)

## TODO
- Implement remaining API endpoints
- Enhance error handling and logging
- Add comprehensive documentation
- Implement pagination handling
- Add integration tests
- Optimize for performance
- Implement rate limiting and caching

## Notes for Developers
- Always check for UserId in multiple possible locations in API responses
- Include DID in requests when available for better request tracking
- Use type hints and docstrings for better code readability and IDE support
- Regularly update tests to cover new functionality and edge cases
