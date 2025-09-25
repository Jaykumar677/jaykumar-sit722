import os, uuid, requests

RUN_ID = os.getenv("RUN_ID", "local")

CUSTOMER_URL = os.getenv("CUSTOMER_URL")
ORDER_URL = os.getenv("ORDER_URL")
PRODUCT_URL = os.getenv("PRODUCT_URL")

if not CUSTOMER_URL or not ORDER_URL or not PRODUCT_URL:
    CUSTOMER_URL = f"http://customer-service-staging-{RUN_ID}.australiaeast.azurecontainer.io:8000"
    ORDER_URL = f"http://order-service-staging-{RUN_ID}.australiaeast.azurecontainer.io:8000"
    PRODUCT_URL = f"http://product-service-staging-{RUN_ID}.australiaeast.azurecontainer.io:8000"

# Health checks
def test_customer_service(): assert requests.get(f"{CUSTOMER_URL}/health").status_code == 200
def test_order_service():    assert requests.get(f"{ORDER_URL}/health").status_code == 200
def test_product_service():  assert requests.get(f"{PRODUCT_URL}/health").status_code == 200

# CRUD
def test_customer_crud():
    email = f"test-{uuid.uuid4().hex[:6]}@example.com"
    new_customer = {"email": email,"first_name":"Test","last_name":"User","password":"secret1234","phone_number":"1234567890","shipping_address":"123 Test Street"}

    r = requests.post(f"{CUSTOMER_URL}/customers", json=new_customer); assert r.status_code in [200,201]
    cid = r.json()["customer_id"]

    r = requests.get(f"{CUSTOMER_URL}/customers/{cid}"); assert r.status_code==200 and r.json()["email"]==email
    r = requests.put(f"{CUSTOMER_URL}/customers/{cid}", json={"first_name":"Updated"}); assert r.status_code==200
    assert requests.get(f"{CUSTOMER_URL}/customers/{cid}").json()["first_name"]=="Updated"
    assert requests.delete(f"{CUSTOMER_URL}/customers/{cid}").status_code in [200,204]
    assert requests.get(f"{CUSTOMER_URL}/customers/{cid}").status_code==404
