from fastapi import FastAPI
from datetime import date

app = FastAPI()

cars = ["TOYOTA", "BMW", "MERCEDES", "HYUNDAI"]
rentedCars = []

@app.get("/dateAvaiblesCars")
def dateAvaiablesCars(date: date):
    return 

@app.post("/rentCar")
def rentCar(car: str, date: date):
    if (car in cars and car not in rentedCars[0]) or (car in cars and car in rentedCars[0] and date not in rentedCars[1]):
        rentedCars.append((car, date))
        return f"Car {car} rented successfully for {date.strftime("%Y-%m-%d")}"
    else:
        return f"Car {car} not available for {date.strftime("%Y-%m-%d")}"