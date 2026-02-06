---
applyTo: '**/test_*.py'
---
# How to write unit-tests

## Test organization

* `tests/unit` → pure logic tests (no FastAPI server)
* `tests/integration` → component interaction
* `tests/functional` → end-to-end API behavior
* `tests/api` → endpoint-focused tests

Each test class should target **one feature or endpoint**.


## Test structure

Tests should:

1. **Given** — prepare fixtures and mocks
2. **When** — execute the action
3. **Then** — assert results

Use:

* `pytest`
* fixtures for setup
* `unittest.mock.patch` for mocking dependencies
* FastAPI test client for API tests

### Example style (reference)

Use this structure as a template:

```python
def test_when_condition_then_expected_result(self, client, dependency):
    # Given
    with patch.object(dependency, "method", return_value=value):

        # When
        response = client.get("/endpoint")

        # Then
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
```
## Testing guidelines (very important)

All tests must follow a **Given / When / Then** naming and structure.

### Naming convention

Test methods must be named like:

```
test_when_<condition>_then_<expected_result>
```

Example:

```
test_when_deps_are_not_ready_then_is_ready_returns_503
```
