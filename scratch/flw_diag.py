"""
Diagnostic script - run as:
  python scratch/flw_diag.py
from the komunityWeb directory with the virtualenv activated.
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

import requests
from django.conf import settings

TOKEN_URL = "https://idp.flutterwave.com/realms/flutterwave/protocol/openid-connect/token"
SANDBOX_BASE = "https://developersandbox-api.flutterwave.com"

print("="*60)
print("STEP 1: Fetching OAuth token")
print("="*60)
payload = {
    'client_id': settings.FLW_CLIENT_ID,
    'client_secret': settings.FLW_CLIENT_SECRET,
    'grant_type': 'client_credentials'
}
r = requests.post(TOKEN_URL, data=payload, headers={'Content-Type': 'application/x-www-form-urlencoded'}, timeout=15)
print(f"Status: {r.status_code}")
token_data = r.json()
print(f"Response keys: {list(token_data.keys())}")
token = token_data.get('access_token')
if not token:
    print("ERROR: No access_token in response!")
    print(token_data)
    sys.exit(1)
print(f"Token (first 30 chars): {token[:30]}...")

print()
print("="*60)
print("STEP 2a: Create a customer to get a customer_id")
print("="*60)
cust_url = f"{SANDBOX_BASE}/customers"
cust_payload = {
    "email": "test@komunity.com",
    "name": {"first": "Test", "last": "User"},
    "phone": {"country_code": "27", "number": "100001001"}
}
auth_headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json',
    'X-Trace-Id': 'komunity-diag-cust-001'
}
rc = requests.post(cust_url, json=cust_payload, headers=auth_headers, timeout=15)
print(f"HTTP Status: {rc.status_code}")
cust_data = rc.json()
print(f"Response: {cust_data}")
customer_id = (cust_data.get('data') or {}).get('id')
if not customer_id:
    # Try searching for existing customer
    rs = requests.get(f"{cust_url}?email=test%40komunity.com", headers=auth_headers, timeout=15)
    search_data = rs.json()
    print(f"Search response: {search_data}")
    items = search_data.get('data') or []
    if isinstance(items, dict):
        items = items.get('items') or []
    if items:
        customer_id = items[0].get('id')
print(f"Using customer_id: {customer_id}")

print()
print("="*60)
print("STEP 2b: Create a payment method for the customer")
print("="*60)
pm_url = f"{SANDBOX_BASE}/payment-methods"
pm_payload = {
    "type": "mobile_money",
    "customer_id": customer_id,
    "mobile_money": {
        "network": "MTN",
        "country_code": "233",
        "phone_number": "100001001"
    }
}
pm_resp = requests.post(pm_url, json=pm_payload, headers=auth_headers, timeout=15)
print(f"HTTP Status: {pm_resp.status_code}")
pm_data = pm_resp.json()
print(f"Response: {pm_data}")
payment_method_id = (pm_data.get('data') or {}).get('id')
print(f"Using payment_method_id: {payment_method_id}")

print()
print("="*60)
print("STEP 2c: Charge using customer_id + payment_method_id + X-Scenario-Key")
print("="*60)
url = f"{SANDBOX_BASE}/charges"
charge_payload = {
    "amount": 100.0,
    "currency": "GHS",
    "reference": "diag-test-005",
    "customer_id": customer_id,
    "payment_method_id": payment_method_id,
    "meta": {"voucher_pin": "19203804939000", "source": "komunity_wallet"}
}
charge_headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json',
    'X-Scenario-Key': 'scenario:charge.succeeded',
    'X-Trace-Id': 'komunity-diag-charge-001'
}
print(f"POST {url}")
print(f"customer_id={customer_id}, payment_method_id={payment_method_id}")
r2 = requests.post(url, json=charge_payload, headers=charge_headers, timeout=15)
print(f"\nHTTP Status: {r2.status_code}")
try:
    print(r2.json())
except Exception:
    print(r2.text)
