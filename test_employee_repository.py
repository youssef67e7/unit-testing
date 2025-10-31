import unittest
from unittest.mock import patch, Mock
from employee_repository import EmployeeRepository, EmployeeRepositoryError


SAMPLE_EMPLOYEES_UNSORTED = [
    {"id": 3, "name": "Alice", "position": "Developer"},
    {"id": 1, "name": "Bob", "position": "Manager"},
    {"id": 2, "name": "Charlie", "position": "Designer"}
]

SAMPLE_EMPLOYEES_SORTED = [
    {"id": 1, "name": "Bob", "position": "Manager"},
    {"id": 2, "name": "Charlie", "position": "Designer"},
    {"id": 3, "name": "Alice", "position": "Developer"}
]


class TestEmployeeRepository(unittest.TestCase):
    """Unit tests for EmployeeRepository using unittest.mock to avoid network calls."""

    def setUp(self) -> None:
        self.repo = EmployeeRepository()

    @staticmethod
    def _make_mock_response(status_code: int, json_data=None) -> Mock:
        mock_resp = Mock()
        mock_resp.status_code = status_code
        mock_resp.json.return_value = json_data
        return mock_resp

    @patch("requests.get")
    def test_successful_retrieval_returns_sorted_list(self, mock_get):
        """
        When the API returns 200 and a list of employees, get_employees() should
        return the employees sorted ascending by id.
        """
        mock_get.return_value = self._make_mock_response(200, SAMPLE_EMPLOYEES_UNSORTED)

        result = self.repo.get_employees()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
        self.assertEqual(result, SAMPLE_EMPLOYEES_SORTED)
        # explicit checks on first and last items for readability
        self.assertEqual(result[0]["id"], 1)
        self.assertEqual(result[-1]["id"], 3)

    @patch("requests.get")
    def test_sorting_stable_and_consistent_with_int_ids(self, mock_get):
        """
        Ensure sorting uses integer IDs and is stable: if ids equal, original order preserved.
        """
        # create a list with duplicate id to check stability
        duplicated = [
            {"id": "2", "name": "First", "position": "X"},
            {"id": 1, "name": "Bob", "position": "Manager"},
            {"id": 2, "name": "Second", "position": "Y"},
        ]
        mock_get.return_value = self._make_mock_response(200, duplicated)

        result = self.repo.get_employees()

        # After sorting by integer value, Bob (id=1) must be first
        self.assertEqual(result[0]["id"], 1)
        # the two with id == 2 should preserve relative order (First then Second)
        self.assertEqual(result[1]["name"], "First")
        self.assertEqual(result[2]["name"], "Second")

    @patch("requests.get")
    def test_error_handling_non_200_raises(self, mock_get):
        """
        If the API responds with a non-200 status code, an EmployeeRepositoryError must be raised.
        """
        mock_get.return_value = self._make_mock_response(500, None)

        with self.assertRaises(EmployeeRepositoryError) as cm:
            self.repo.get_employees()

        self.assertIn("Unexpected status code", str(cm.exception))

    @patch("requests.get")
    def test_error_on_invalid_json_format_raises(self, mock_get):
        """
        If the API returns a JSON that is not a list, raise EmployeeRepositoryError.
        """
        mock_get.return_value = self._make_mock_response(200, {"not": "a list"})

        with self.assertRaises(EmployeeRepositoryError):
            self.repo.get_employees()

    @patch("requests.get")
    def test_network_exception_translated_to_repository_error(self, mock_get):
        """
        Network exceptions raised by requests.get must be translated to EmployeeRepositoryError.
        """
        mock_get.side_effect = Exception("network failure")

        with self.assertRaises(EmployeeRepositoryError) as cm:
            self.repo.get_employees()

        self.assertIn("HTTP request failed", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
