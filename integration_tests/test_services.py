import os
import uuid
import requests
import time

RUN_ID = os.getenv("RUN_ID", "local")

# Try environment variables first (CI passes them for prod)
CUSTOMER_URL = os.getenv("CUSTOMER_URL")
ORDER_URL = os.getenv("ORDER_URL")
PRODUCT_URL = os.getenv("PRODUCT_URL")

# If not provided, fallback to staging URLs
if not CUSTOMER_URL or not ORDER_URL or not PRODUCT_URL:
    CUSTOMER_URL = f"http://customer-service-staging-{RUN_ID}.australiaeast.azurecontainer.io:8000"
    ORDER_URL = f"http://order-service-staging-{RUN_ID}.australiaeast.azurecontainer.io:8000"
    PRODUCT_URL = f"http://product-service-staging-{RUN_ID}.australiaeast.azurecontainer.io:8000"


# --- Utility: wait until service is live ---
def wait_for_service(url, retries=30, delay=10):
    """
    Wait for a service /health endpoint to respond with 200.
    Retries for up to retries*delay seconds.
    """
    for i in range(retries):
        try:
            r = requests.get(f"{url}/health", timeout=5)
            if r.status_code == 200:
                print(f"✅ {url} is healthy")
                return
        except Exception as e:
            print(f"⏳ Waiting for {url} ({e})")
        time.sleep(delay)
    raise RuntimeError(f"❌ Service at {url} not responding after {retries*delay}s")


# Run before all tests
def setup_module(module):
    wait_for_service(CUSTOMER_URL)
    wait_for_service(ORDER_URL)
    wait_for_service(PRODUCT_URL)


# --- Health checks ---
def test_customer_service():
    assert requests.get(f"{CUSTOMER_URL}/health").status_code == 200

def test_order_service():
    assert requests.get(f"{ORDER_URL}/health").status_code == 200

def test_product_service():
    assert requests.get(f"{PRODUCT_URL}/health").status_code == 200


# --- CRUD tests for customer service ---
def test_customer_crud():
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
    r = requests.post(f"{CUSTOMER_URL}/customers/", json=new_customer)
    assert r.status_code in [200, 201], f"Create failed: {r.text}"
    cid = r.json()["customer_id"]

    # Read
    r = requests.get(f"{CUSTOMER_URL}/customers/{cid}")
    assert r.status_code == 200 and r.json()["email"] == email

    # Update
    r = requests.put(f"{CUSTOMER_URL}/customers/{cid}", json={"first_name": "Updated"})
    assert r.status_code == 200
    r = requests.get(f"{CUSTOMER_URL}/customers/{cid}")
    assert r.json()["first_name"] == "Updated"

    # Delete
    r = requests.delete(f"{CUSTOMER_URL}/customers/{cid}")
    assert r.status_code in [200, 204]
    r = requests.get(f"{CUSTOMER_URL}/customers/{cid}")
    assert r.status_code == 404
