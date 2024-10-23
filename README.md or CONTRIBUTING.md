## Import Structure

When working with the haaslib package, please adhere to the following import structure:

- `RequestsExecutor`, `HaasApiError`, `AuthenticationError`, `Guest`, and `Authenticated` should be imported from `haaslib.api`.
- Do not import `Guest` or `Authenticated` from `haaslib.model`.

Example of correct imports:

```python
from haaslib.api import RequestsExecutor, HaasApiError, AuthenticationError, Guest, Authenticated
```
