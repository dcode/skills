# Good and Bad Tests

Examples use Python and pytest; the principles hold in any language and test framework.

## Good Tests

**Integration-style**: test through real interfaces, not mocks of internal parts.

```python
# GOOD: tests observable behavior
def test_user_can_checkout_with_valid_cart() -> None:
    cart = Cart()
    cart.add(product)
    result = checkout(cart, payment_method)
    assert result.status == "confirmed"
```

Characteristics:

- Tests behavior users/callers care about
- Uses the public interface only
- Survives internal refactors
- Describes WHAT, not HOW
- One logical assertion per test

## Bad Tests

**Implementation-detail tests**: coupled to internal structure.

```python
# BAD: tests implementation details
def test_checkout_calls_payment_service_process(mocker) -> None:
    process = mocker.patch("shop.checkout.payment_service.process")
    checkout(cart, payment)
    process.assert_called_once_with(cart.total)
```

Red flags:

- Mocking internal collaborators
- Testing private methods
- Asserting on call counts/order
- Test breaks when refactoring without behavior change
- Test name describes HOW not WHAT
- Verifying through external means instead of the interface

```python
# BAD: bypasses the interface to verify
def test_create_user_saves_to_database(db) -> None:
    create_user(name="Alice")
    row = db.execute("SELECT * FROM users WHERE name = ?", ("Alice",)).fetchone()
    assert row is not None


# GOOD: verifies through the interface
def test_created_user_is_retrievable() -> None:
    user = create_user(name="Alice")
    assert get_user(user.id).name == "Alice"
```

**Tautological tests**: the expected value restates the implementation, so the test passes by construction.

```python
# BAD: expected value is recomputed the way the code computes it
def test_calculate_total_sums_line_items() -> None:
    items = [LineItem(price=10), LineItem(price=5)]
    expected = sum(item.price for item in items)
    assert calculate_total(items) == expected


# GOOD: expected value is an independent, known literal
def test_calculate_total_sums_line_items() -> None:
    assert calculate_total([LineItem(price=10), LineItem(price=5)]) == 15
```
