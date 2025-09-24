import os
import requests

RUN_ID = os.getenv("RUN_ID")

# Base URLs for services (use RUN_ID injected by GitHub Actions)
CUSTOMER_URL = f"http://customer-service-prod-{RUN_ID}.australiaeast.azurecontainer.io:8000"
ORDER_URL = f"http://order-service-prod-{RUN_ID}.australiaeast.azurecontainer.io:8000"
PRODUCT_URL = f"http://product-service-prod-{RUN_ID}.australiaeast.azurecontainer.io:8000"

def test_customer_service():
    url = f"{CUSTOMER_URL}/health"
    response = requests.get(url)
    assert response.status_code == 200

def test_order_service():
    url = f"{ORDER_URL}/health"
    response = requests.get(url)
    assert response.status_code == 200

def test_product_service():
    url = f"{PRODUCT_URL}/health"
    response = requests.get(url)
    assert response.status_code == 200

def test_customer_crud():
    # Example: CRUD test on customer service
    create_url = f"{CUSTOMER_URL}/customers"
    new_customer = {"name": "Test User", "email": "test@example.com"}
    r = requests.post(create_url, json=new_customer)
    assert r.status_code == 200
    customer_id = r.json().get("id")

    # Fetch created customer
    r = requests.get(f"{CUSTOMER_URL}/customers/{customer_id}")
    assert r.status_code == 200
    assert r.json()["email"] == "test@example.com"
