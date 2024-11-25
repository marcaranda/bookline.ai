from fastapi import FastAPI
from datetime import date

app = FastAPI()

cars = ["TOYOTA", "BMW", "MERCEDES", "HYUNDAI"]
rentedCars = []

@app.get("/dateAvaiblesCars")
def dateAvaiablesCars(date: date):
    avaiblesCars = [car for car in cars if car not in [rentedCar[0] for rentedCar in rentedCars if rentedCar[1] == date]]
    return {f"Available cars for {date.strftime('%Y-%m-%d')}": avaiblesCars}

@app.post("/rentCar")
def rentCar(car: str, date: date):
    if car in cars:
      if car not in [rentedCar[0] for rentedCar in rentedCars if rentedCar[1] == date]:
          rentedCars.append((car, date))
          return f"Car {car} rented successfully for {date.strftime('%Y-%m-%d')}"
      else:
          return f"Car {car} not available for {date.strftime('%Y-%m-%d')}"
    else:
        return f"We do not have the car {car} available for rent"