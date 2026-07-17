from django.test import TestCase
from wallet.flutterwave import get_access_token, charge_voucher, initiate_transfer
import uuid

class FlutterwaveIntegrationTest(TestCase):
    def test_oauth_token_retrieval(self):
        try:
            token = get_access_token()
            self.assertIsNotNone(token)
            self.assertTrue(len(token) > 0)
            print("\n[SUCCESS] OAuth Token retrieved from Flutterwave Sandbox!")
        except Exception as e:
            self.fail(f"OAuth Token retrieval failed: {e}")

    def test_voucher_charge_graceful_fail(self):
        # We test with an invalid pin to make sure the endpoint receives our request
        # and returns a structured validation/auth response rather than crashing.
        ref = f"test-topup-{uuid.uuid4().hex[:8]}"
        res = charge_voucher(
            voucher_pin="9999999999999999",  # Mock invalid pin
            amount=100.00,
            email="test@komunity.com",
            phone_number="0821234567",
            tx_ref=ref
        )
        self.assertFalse(res['success'])
        self.assertIn('error', res)
        print(f"\n[SUCCESS] Voucher charge failed gracefully as expected: {res['error']}")
