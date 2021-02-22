import unittest
from unittest.mock import Mock, patch

from lambda_src import main


class Handler(unittest.TestCase):
    def setUp(self) -> None:
        # Arrange
        self.mock_method = Mock()
        self.mock_path = Mock()
        self.mock_handler_fn = Mock()

        # setup the ROUTER so that it has an entry for the method/path/handler
        patch.dict('lambda_src.main.ROUTER', {
            self.mock_method: {
                self.mock_path: self.mock_handler_fn
            }
        }).start()

        self.mock_event = "MOCK_EVENT"
        self.mock_context = self.make_context(self.mock_method, self.mock_path)

    def tearDown(self) -> None:
        patch.stopall()

    """main.handler"""
    def make_context(self, http_method, path):
        return {
            "requestContext": {
                "httpMethod": http_method,
                "path": path,
            },
        }

    def test_calls_handler_fn_when_found(self):
        """
        calls the appropriate handler function when it exists in the ROUTER
        """
        # Act
        main.handler(self.mock_event, self.mock_context)

        # Assert
        self.mock_handler_fn.assert_called_once_with(self.mock_event, self.mock_context)

    def test_returns_handler_fn_result(self):
        """
        returns the result of the call to the selected handler function
        """
        # Act
        response = main.handler(self.mock_event, self.mock_context)

        # Assert
        self.assertEqual(response, self.mock_handler_fn.return_value)

    def test_handler_raises_exception_on_unknown_method(self):
        """
        raises an exception when httpMethod is of unknown type
        """
        # Arrange
        mock_context = self.make_context(Mock(), Mock())

        # Act / Assert
        with self.assertRaises(Exception):
            main.handler(self.mock_event, mock_context)

    def test_handler_raises_exception_on_unknown_path(self):
        """
        raises an exception when httpMethod is valid but path is not
        """
        # Arrange
        mock_context = self.make_context(http_method=self.mock_method, path=Mock())

        # Act / Assert
        with self.assertRaises(Exception):
            main.handler(self.mock_event, mock_context)