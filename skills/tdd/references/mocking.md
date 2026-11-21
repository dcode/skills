# When to Mock

Mock at **system boundaries** only:

- External APIs (payment, email, etc.)
- Databases (sometimes; prefer a real test database or an in-memory one)
- Time and randomness
- File system (sometimes; prefer a temp directory such as pytest's `tmp_path`)

Don't mock:

- Your own classes or modules
- Internal collaborators
- Anything you control

## Designing for Mockability

At system boundaries, design interfaces that are easy to replace in tests.

### 1. Use dependency injection

Pass external dependencies in rather than creating them internally:

```python
# Easy to mock: the caller (or test) supplies the client
def process_payment(order: Order, payments: PaymentClient) -> Charge:
    return payments.charge(order.total)


# Hard to mock: the dependency and its config are created inside
def process_payment(order: Order) -> Charge:
    client = StripeClient(os.environ["STRIPE_KEY"])
    return client.charge(order.total)
```

### 2. Prefer SDK-style interfaces over generic fetchers

Create one method per external operation instead of one generic function with conditional logic:

```python
# GOOD: each method is independently replaceable with a fake
class UsersApi(Protocol):
    def get_user(self, user_id: str) -> User: ...
    def get_orders(self, user_id: str) -> list[Order]: ...
    def create_order(self, data: NewOrder) -> Order: ...


# BAD: a fake needs branching on the endpoint to return the right shape
class Api(Protocol):
    def fetch(self, endpoint: str, **options: Any) -> dict[str, Any]: ...
```

The SDK approach means:

- Each fake returns one specific shape
- No conditional logic in test setup
- Easier to see which operations a test exercises
- Type checking per operation

A hand-written fake class that satisfies the protocol is usually clearer than a `unittest.mock.Mock`, and a type checker
verifies it still matches the interface.
