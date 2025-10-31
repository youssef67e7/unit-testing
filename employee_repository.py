from typing import List, Dict, Optional
import requests


class EmployeeRepositoryError(Exception):
    """Raised when EmployeeRepository cannot retrieve employees."""
    pass


class EmployeeRepository:
    """
    Simple repository to fetch and return employees sorted by 'id'.
    - On success (HTTP 200) returns List[Dict].
    - On failure raises EmployeeRepositoryError.
    """

    EMPLOYEES_URL = "https://api.example.com/employees"
    TIMEOUT = 5  # seconds

    def get_employees(self) -> List[Dict]:
        """
        Fetch employees from external API and return them sorted by 'id'.

        Raises:
            EmployeeRepositoryError: when request fails or non-200 response.
        """
        try:
            response = requests.get(self.EMPLOYEES_URL, timeout=self.TIMEOUT)
        except Exception as exc:
            raise EmployeeRepositoryError("HTTP request failed") from exc

        if response.status_code != 200:
            raise EmployeeRepositoryError(f"Unexpected status code: {response.status_code}")

        employees = response.json()
        if not isinstance(employees, list):
            raise EmployeeRepositoryError("Invalid response format: expected a list")

        try:
            return sorted(employees, key=lambda e: int(e["id"]))
        except (KeyError, TypeError, ValueError) as exc:
            raise EmployeeRepositoryError("Invalid employee data format") from exc
