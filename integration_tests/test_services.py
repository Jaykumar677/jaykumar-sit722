import os
import requests

RUN_ID = os.getenv("RUN_ID")

def test_customer_service():
    url = f"http://customer-service-{RUN_ID}.australiaeast.azurecontainer.io:8000/health"
    response = requests.get(url)
    assert response.status_code == 200

def test_order_service():
    url = f"http://order-service-{RUN_ID}.australiaeast.azurecontainer.io:8000/health"
    response = requests.get(url)
    assert response.status_code == 200

def test_product_service():
    url = f"http://product-service-{RUN_ID}.australiaeast.azurecontainer.io:8000/health"
    response = requests.get(url)
    assert response.status_code == 200

def test_customer_crud():
    base_url = f"http://customer-service-{RUN_ID}.australiaeast.azurecontainer.io:8000/customers"
    
    # Create customer
    new_customer = {"name": "Test User", "email": "test@example.com"}
    r = requests.post(base_url, json=new_customer)
    assert r.status_code == 200
    customer_id = r.json().get("id")

    # Fetch customer
    r = requests.get(f"{base_url}/{customer_id}")
    assert r.status_code == 200
    assert r.json()["email"] == "test@example.com"
