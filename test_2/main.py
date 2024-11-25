from fastapi import FastAPI
from datetime import date
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

@app.get("/dateAvaiblesCars")
def date_avaiables_cars(date: date):
  rentedCarsList = load_rented_cars_list()

  # Get the cars that are not rented for the date
  avaiblesCars = [car for car in cars if car not in [rentedCar["car"] for rentedCar in rentedCarsList if rentedCar["rentalDate"] == date.strftime('%Y-%m-%d')]]

  logging.info(f"User queried available cars for date: {date}")
  if len(avaiblesCars) > 0:
    return {f"Available cars for {date}": avaiblesCars}
  else:
    return {f"Non available cars for {date}"}

@app.post("/rentCar")
def rent_car(car: str, date: date):
  # Check if the car is at the cars list, else return an error message
  if car in cars:
    rentedCarsList = load_rented_cars_list()

    # Check if the car is available for the date, else return an error message
    if car not in [rentedCar["car"] for rentedCar in rentedCarsList if rentedCar["rentalDate"] == date.strftime('%Y-%m-%d')]:
        # Append the new rented car to the list   
        rentedCar = {
            "car": car,
            "rentalDate": date.strftime('%Y-%m-%d')
        }
        rentedCarsList.append(rentedCar)

        # Save the rented cars list to database
        with open('database.json', 'w') as json_file:
            json.dump(rentedCarsList, json_file)

        logging.info(f"User rented a car: {car} - {date}")
        return f"Car {car} rented successfully for {date.strftime('%Y-%m-%d')}."
    else:
        logging.error(f"User tried to rent a car that is already rented for that date: {car} - {date}")
        return f"Car {car} not available for {date.strftime('%Y-%m-%d')}."
  else:
      logging.error(f"User tried to rent a car that is not in out cars list: {car}")
      return f"We do not have the car {car} available for rent."