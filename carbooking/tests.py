import json
from django.test import TestCase
from django.urls import reverse


class RegisterApiTestCase(TestCase):
    def test_register_endpoint(self):
        """
        Test case for the user registration API endpoint.

        This test verifies that a user can successfully register by sending
        valid email, password, and name data. It expects a 201 Created
        response with a token in the response body, confirming that the
        registration process works as intended.

        The test also prints the response status code and content for debugging
        purposes, helping to diagnose issues if the response does not match
        expectations.
        """
        url = reverse('register')
        data = {
            "email": "testuser@example.com",
            "password": "Password123",
            "name": "Test User"
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        print('Status code:', response.status_code)
        try:
            print('Response JSON:', response.json())
        except Exception as e:
            print('Error parsing JSON response:', e)
            print('Response content:', response.content)

        self.assertEqual(response.status_code, 201)
        self.assertIn('token', response.json())
