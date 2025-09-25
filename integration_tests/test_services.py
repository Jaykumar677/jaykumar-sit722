import os, uuid, requests, time

# Static IPs from your running ACI containers
CUSTOMER_URL = os.getenv("CUSTOMER_URL", "http://4.237.151.181:8000")
ORDER_URL    = os.getenv("ORDER_URL", "http://20.167.3.34:8000")
PRODUCT_URL  = os.getenv("PRODUCT_URL", "http://4.254.28.231:8000")

def wait_for_service(url, retries=60, delay=5):
    for i in range(retries):
        try:
            r = requests.get(f"{url}/health", timeout=5)
            if r.status_code == 200:
                print(f"✅ {url} is healthy")
                return
        except Exception as e:
            print(f"⏳ Waiting for {url} ({e}) [{i+1}/{retries}]")
        time.sleep(delay)
    raise RuntimeError(f"❌ Service at {url} not responding after {retries*delay}s")

def setup_module(module):
    # Ensure all services are up before running tests
    wait_for_service(CUSTOMER_URL)
    wait_for_service(ORDER_URL)
    wait_for_service(PRODUCT_URL)

# Health checks
def test_customer_service():
    assert requests.get(f"{CUSTOMER_URL}/health").status_code == 200

def test_order_service():
    assert requests.get(f"{ORDER_URL}/health").status_code == 200

def test_product_service():
    assert requests.get(f"{PRODUCT_URL}/health").status_code == 200

# CRUD test for Customer Service
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
    r = requests.post(f"{CUSTOMER_URL}/customers", json=new_customer)
    assert r.status_code in [200, 201]
    cid = r.json()["customer_id"]

    # Read
    r = requests.get(f"{CUSTOMER_URL}/customers/{cid}")
    assert r.status_code == 200 and r.json()["email"] == email

    # Update
    r = requests.put(f"{CUSTOMER_URL}/customers/{cid}", json={"first_name": "Updated"})
    assert r.status_code == 200
    assert requests.get(f"{CUSTOMER_URL}/customers/{cid}").json()["first_name"] == "Updated"

    # Delete
    assert requests.delete(f"{CUSTOMER_URL}/customers/{cid}").status_code in [200, 204]
    assert requests.get(f"{CUSTOMER_URL}/customers/{cid}").status_code == 404
