from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

# Test cases
def test_date_avaiables_cars_ok():
  response_1 = client.get("/dateAvaiblesCars?date=2024-12-24")
  assert response_1.status_code == 200
  assert response_1.json() == {"Available cars for 2024-12-24": ["TOYOTA", "BMW", "MERCEDES", "HYUNDAI"]}

  response_2 = client.get("/dateAvaiblesCars?date=2024-12-25")
  assert response_2.status_code == 200
  assert response_2.json() == {"Available cars for 2024-12-25": ["TOYOTA", "MERCEDES", "HYUNDAI"]}

  response_3 = client.get("/dateAvaiblesCars?date=2024-12-26")
  assert response_3.status_code == 200
  assert response_3.json() == {"Available cars for 2024-12-26": ["TOYOTA", "HYUNDAI"]}

  response_4 = client.get("/dateAvaiblesCars?date=2024-12-27")
  assert response_4.status_code == 200
  assert response_4.json() == ["Non available cars for 2024-12-27"]

def test_date_avaiables_cars_incorrect_date():
  response = client.get("/dateAvaiblesCars?date=2024")
  assert response.status_code == 422