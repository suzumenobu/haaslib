
# haaslib

Rust client for [HaasOnline](https://www.haasonline.com/) API. Enables automating and interacting with Haas trading infrastructure.

## Features

- API Client handles communication
- Utilities to create, execute, monitor backtests
- Structs for key entities like markets, accounts
- Custom result handling

## Usage

First construct an API client instance and authenticate:

```rust
let mut api = Api::new("127.0.0.1".to_string(), "8080".to_string(), "http".to_string());
api.app_login("user@email.com", "secretkey123");
```

Then use the API methods: 

```rust
// Fetch available market data
let markets = api.all_markets()?;

// Choose a market + parameters for backtest  
let create_lab_request = CreateLabRequest {
    script_id: "some-script",
    name: "My Backtest",
    market: &markets[0],
    // other params    
};

// Create Lab for backtest   
let details = api.create_lab(create_lab_request)?;

// Start execution  
api.start_lab_execution(details.lab_id);   

// Get detailed results
let results = api.get_backtest_result::<MyCustomReport>(details.lab_id);
```

The `lab` module provides utilities for common backtesting workflows.

See the full [API docs](https://docs.rs/haaslib) for available methods and detailed usage.  

## License

This project is licensed under the MIT license.

Let me know if any other sections would be useful to add or if an example should be expanded/clarified! Tried to provide basic overview and configuration to help users get started.
