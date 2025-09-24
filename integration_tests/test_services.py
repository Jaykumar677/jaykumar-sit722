import os
import requests

# Get RUN_ID from environment variable (injected by GitHub Actions)
RUN_ID = os.getenv("RUN_ID")

# Base URLs for services (use RUN_ID to form DNS name)
ORDER_URL = f"http://order-service-{RUN_ID}.australiaeast.azurecontainer.io:8000"
CUSTOMER_URL = f"http://customer-service-{RUN_ID}.australiaeast.azurecontainer.io:8000"
PRODUCT_URL = f"http://product-service-{RUN_ID}.australiaeast.azurecontainer.io:8000"


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
    # Create customer
    new_customer = {"name": "Test User", "email": "test@example.com"}
    r = requests.post(f"{CUSTOMER_URL}/customers", json=new_customer)
    assert r.status_code == 200
    customer_id = r.json().get("id")

    # Fetch customer
    r = requests.get(f"{CUSTOMER_URL}/customers/{customer_id}")
    assert r.status_code == 200
    assert r.json()["email"] == "test@example.com"
