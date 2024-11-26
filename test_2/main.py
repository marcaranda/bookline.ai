from fastapi import FastAPI, HTTPException
from datetime import date
import pydantic
import json
import os
import logging

logging.basicConfig(filename='main.log',
                    filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

app = FastAPI()

cars = ["TOYOTA", "BMW", "MERCEDES", "HYUNDAI"]

def load_rented_cars_list():
    # If database.json contains the rented cars list, load it, else create an empty list
    if os.stat('database.json').st_size > 0:
        with open('database.json') as json_file:
            return json.load(json_file)
    else:
        return []

@app.get("/dateAvailableCars")
def date_available_cars(date: date):
  rentedCarsList = load_rented_cars_list()

  # Get the cars that are not rented for the date
  availableCars = [car for car in cars if car not in [rentedCar["car"] for rentedCar in rentedCarsList if rentedCar["rentalDate"] == date.strftime('%Y-%m-%d')]]

  logging.info(f"User queried available cars for date: {date}")
  if len(availableCars) > 0:
    return {f"Available cars for {date}": availableCars}
  else:
    return f"Non available cars for {date}"

class CarRental(pydantic.BaseModel):
    car: str
    date: date

@app.post("/rentCar")
def rent_car(carRental: CarRental):
  # Check if the car is at the cars list, else return an error message
  if carRental.car in cars:
    rentedCarsList = load_rented_cars_list()

    # Check if the car is available for the date, else return an error message
    if carRental.car not in [rentedCar["car"] for rentedCar in rentedCarsList if rentedCar["rentalDate"] == carRental.date.strftime('%Y-%m-%d')]:
        # Append the new rented car to the list
        rentedCarsList.append({
            "car": carRental.car,
            "rentalDate": carRental.date.strftime('%Y-%m-%d')
        })

        # Save the rented cars list to database
        with open('database.json', 'w') as json_file:
            json.dump(rentedCarsList, json_file)

        logging.info(f"User rented a car: {carRental.car} - {carRental.date.strftime('%Y-%m-%d')}")
        return f"Car {carRental.car} rented successfully for {carRental.date.strftime('%Y-%m-%d')}."
    else:
        logging.error(f"User tried to rent a car that is already rented for that date: {carRental.car} - {carRental.date.strftime('%Y-%m-%d')}")
        return f"Car {carRental.car} not available for {carRental.date.strftime('%Y-%m-%d')}."
  else:
      logging.error(f"User tried to rent a car that is not in out cars list: {carRental.car}")
      raise HTTPException(status_code=404, detail=f"Car {carRental.car} not found.")