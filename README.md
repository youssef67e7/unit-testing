# Employee Repository Unit Testing

This repository contains a Python class [EmployeeRepository](employee_repository.py) that fetches employee data from an external API and sorts them by ID, along with comprehensive unit tests in [test_employee_repository.py](test_employee_repository.py).

## Files

- `employee_repository.py`: Contains the EmployeeRepository class that handles fetching and sorting employee data
- `test_employee_repository.py`: Contains unit tests for the EmployeeRepository class using unittest.mock to avoid network calls

## Running Tests

To run the tests, execute:
```bash
python -m unittest test_employee_repository.py
```