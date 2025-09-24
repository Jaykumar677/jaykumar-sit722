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
    new_customer = {
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "secret1234",   # must be >= 8 chars
        "phone_number": "1234567890",
        "shipping_address": "123 Test Street"
    }
    r = requests.post(create_url, json=new_customer)
    assert r.status_code == 200


    # Fetch created customer
    r = requests.get(f"{CUSTOMER_URL}/customers/{customer_id}")
    assert r.status_code == 200
    assert r.json()["email"] == "test@example.com"
