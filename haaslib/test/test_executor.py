import unittest
from unittest.mock import Mock, patch
from ..executor import RequestsExecutor, Guest, Authenticated
from ..exceptions import HaasApiError, AuthenticationError
from ..models.base import ApiResponse

class TestExecutor(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.executor = RequestsExecutor(
            host="127.0.0.1",
            port=8090,
            state=Guest()
        )

    @patch('requests.Session.request')
    def test_execute_success(self, mock_request):
        """Test successful API request execution"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "Success": True,
            "Data": {"test": "data"}
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        response = self.executor.execute(
            endpoint="Price",
            response_type=dict,
            query_params={"channel": "TEST"}
        )
        
        self.assertTrue(response.Success)
        self.assertEqual(response.Data, {"test": "data"})

    @patch('requests.Session.request')
    def test_execute_failure(self, mock_request):
        """Test failed API request execution"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "Success": False,
            "Error": "Test error"
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        response = self.executor.execute(
            endpoint="Price",
            response_type=dict,
            query_params={"channel": "TEST"}
        )
        
        self.assertFalse(response.Success)
        self.assertEqual(response.Error, "Test error")

    @patch('requests.Session.request')
    def test_authentication(self, mock_request):
        """Test authentication process"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "Success": True,
            "Data": {
                "UserId": "test_user",
                "InterfaceKey": "test_key"
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        authenticated = self.executor.authenticate(
            email="test@example.com",
            password="password"
        )
        
        self.assertIsInstance(authenticated.state, Authenticated)
        self.assertEqual(authenticated.state.user_id, "test_user")
        self.assertEqual(authenticated.state.interface_secret, "test_key")
