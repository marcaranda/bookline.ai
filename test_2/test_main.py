# On the terminal, run the following command to execute the tests: pytest test_2/test_main.py

from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

# Test cases

# Test cases for the date_avaiables_cars function

# Date with available cars
def test_date_avaiables_cars_ok():
  response_1 = client.get("/dateAvailableCars?date=2024-12-24")
  assert response_1.status_code == 200
  assert response_1.json() == {"Available cars for 2024-12-24": ["TOYOTA", "BMW", "MERCEDES", "HYUNDAI"]}

  response_2 = client.get("/dateAvailableCars?date=2024-12-25")
  assert response_2.status_code == 200
  assert response_2.json() == {"Available cars for 2024-12-25": ["TOYOTA", "MERCEDES", "HYUNDAI"]}

  response_3 = client.get("/dateAvailableCars?date=2024-12-26")
  assert response_3.status_code == 200
  assert response_3.json() == {"Available cars for 2024-12-26": ["TOYOTA", "HYUNDAI"]}

# Date with no available cars
def test_date_avaiables_cars_no_available_cars():
  response = client.get("/dateAvailableCars?date=2024-12-27")
  assert response.status_code == 200
  assert response.json() == "Non available cars for 2024-12-27"

# Incorrect date format
def test_date_avaiables_cars_incorrect_date():
  response = client.get("/dateAvailableCars?date=2024")
  assert response.status_code == 422


# Test cases for the rent_car function

# Car rented successfully
def test_rent_car_ok():
  response_pre = client.get("/dateAvailableCars?date=2024-12-23")
  assert response_pre.status_code == 200
  assert response_pre.json() == {"Available cars for 2024-12-23": ["TOYOTA", "BMW", "MERCEDES", "HYUNDAI"]}

  # Delete the rent from the database after running it
  response = client.post("/rentCar", json={"car": "TOYOTA", "date": "2024-12-23"})
  assert response.status_code == 200
  assert response.json() == "Car TOYOTA rented successfully for 2024-12-23."

  response_post = client.get("/dateAvailableCars?date=2024-12-23")
  assert response_post.status_code == 200
  assert response_post.json() == {"Available cars for 2024-12-23": ["BMW", "MERCEDES", "HYUNDAI"]}

# Car not found
def test_rent_car_car_not_found():
  response = client.post("/rentCar", json={"car": "AUDI", "date": "2024-12-23"})
  assert response.status_code == 404
  assert response.json() == {"detail": "Car AUDI not found."}

# Car already rented
def test_rent_car_car_already_rented():
  response = client.post("/rentCar", json={"car": "BMW", "date": "2024-12-25"})
  assert response.status_code == 200
  assert response.json() == "Car BMW not available for 2024-12-25."