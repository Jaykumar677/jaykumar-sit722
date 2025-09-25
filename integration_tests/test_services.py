import os, uuid, requests

# Prefer env vars from GitHub Actions
CUSTOMER_URL = os.getenv("CUSTOMER_API")
ORDER_URL = os.getenv("ORDER_API")
PRODUCT_URL = os.getenv("PRODUCT_API")

# Fallback to staging if not set
if not CUSTOMER_URL or not ORDER_URL or not PRODUCT_URL:
    RUN_ID = os.getenv("RUN_ID", "local")
    CUSTOMER_URL = f"http://customer-service-staging-{RUN_ID}.australiaeast.azurecontainer.io:8000"
    ORDER_URL = f"http://order-service-staging-{RUN_ID}.australiaeast.azurecontainer.io:8000"
    PRODUCT_URL = f"http://product-service-staging-{RUN_ID}.australiaeast.azurecontainer.io:8000"


def test_customer_service():
    url = f"{CUSTOMER_URL}/health"
    r = requests.get(url)
    assert r.status_code == 200


def test_order_service():
    url = f"{ORDER_URL}/health"
    r = requests.get(url)
    assert r.status_code == 200


def test_product_service():
    url = f"{PRODUCT_URL}/health"
    r = requests.get(url)
    assert r.status_code == 200


def test_customer_crud():
    # unique email each run
    email = f"test-{uuid.uuid4().hex[:6]}@example.com"
    new_customer = {
        "email": email,
        "first_name": "Test",
        "last_name": "User",
        "password": "secret1234",
        "phone_number": "1234567890",
        "shipping_address": "123 Test Street"
    }

    # Create
    r = requests.post(f"{CUSTOMER_URL}/customers", json=new_customer)
    assert r.status_code in [200, 201], f"Create failed: {r.text}"
    customer_id = r.json()["customer_id"]

    # Read
    r = requests.get(f"{CUSTOMER_URL}/customers/{customer_id}")
    assert r.status_code == 200, f"Read failed: {r.text}"
    assert r.json()["email"] == email

    # Update
    update_data = {"first_name": "Updated"}
    r = requests.put(f"{CUSTOMER_URL}/customers/{customer_id}", json=update_data)
    assert r.status_code == 200, f"Update failed: {r.text}"
    r = requests.get(f"{CUSTOMER_URL}/customers/{customer_id}")
    assert r.json()["first_name"] == "Updated"

    # Delete
    r = requests.delete(f"{CUSTOMER_URL}/customers/{customer_id}")
    assert r.status_code in [200, 204], f"Delete failed: {r.text}"

    # Confirm deleted
    r = requests.get(f"{CUSTOMER_URL}/customers/{customer_id}")
    assert r.status_code == 404, f"Customer still exists: {r.text}"
