import os
import requests

RUN_ID = os.getenv("RUN_ID")

# Base URLs for services
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
    # 1. Create a new customer
    create_url = f"{CUSTOMER_URL}/customers"
    new_customer = {
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "secret1234",
        "phone_number": "1234567890",
        "shipping_address": "123 Test Street"
    }

    r = requests.post(create_url, json=new_customer)
    assert r.status_code == 200, f"Create failed: {r.text}"

    # Extract created customer_id
    data = r.json()
    customer_id = data["customer_id"]

    # 2. Read the created customer
    r = requests.get(f"{CUSTOMER_URL}/customers/{customer_id}")
    assert r.status_code == 200, f"Read failed: {r.text}"
    assert r.json()["email"] == "test@example.com"

    # 3. Update the customer
    update_data = {"first_name": "Updated"}
    r = requests.put(f"{CUSTOMER_URL}/customers/{customer_id}", json=update_data)
    assert r.status_code == 200, f"Update failed: {r.text}"

    # Confirm update worked
    r = requests.get(f"{CUSTOMER_URL}/customers/{customer_id}")
    assert r.json()["first_name"] == "Updated"

    # 4. Delete the customer
    r = requests.delete(f"{CUSTOMER_URL}/customers/{customer_id}")
    assert r.status_code == 200, f"Delete failed: {r.text}"

    # Confirm deletion
    r = requests.get(f"{CUSTOMER_URL}/customers/{customer_id}")
    assert r.status_code == 404, f"Customer still exists after delete: {r.text}"
