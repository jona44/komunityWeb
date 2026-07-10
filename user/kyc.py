class MockKYCProvider:
    @staticmethod
    def verify_document(first_name, surname, id_number, id_type):
        """
        Simulates verification of identity documents with a KYC provider.
        In a real application, this would make an API call to a provider like Smile ID or Yoti.
        """
        if not id_number or len(id_number.strip()) < 6:
            return False, "Invalid document ID: ID must be at least 6 characters long."
        
        # Simulate check rules
        id_cleaned = id_number.strip().lower()
        if id_cleaned == "000000" or id_cleaned == "test" or id_cleaned == "123456":
            return False, "KYC provider rejected document: potential fake or testing ID."

        # Successful verification simulation
        return True, "Identity verified successfully."
