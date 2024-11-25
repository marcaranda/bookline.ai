from fastapi import FastAPI
from datetime import date
import json
import os

app = FastAPI()

cars = ["TOYOTA", "BMW", "MERCEDES", "HYUNDAI"]

@app.get("/dateAvaiblesCars")
def dateAvaiablesCars(date: date):
    # If database.json contains the rented cars list, load it, else create an empty list
    if os.stat("database.json").st_size > 0:
      with open('database.json') as json_file:
          rentedCarsList = json.load(json_file)
    else:
      rentedCarsList = []

    avaiblesCars = [car for car in cars if car not in [rentedCar["car"] for rentedCar in rentedCarsList if rentedCar["rentalDate"] == date.strftime('%Y-%m-%d')]]
    return {f"Available cars for {date}": avaiblesCars}

@app.post("/rentCar")
def rentCar(car: str, date: date):
    # Check if the car is at the cars list, else return an error message
    if car in cars:
      # If database.json contains the rented cars list, load it, else create an empty list
      if os.stat("database.json").st_size > 0:
        with open('database.json') as json_file:
            rentedCarsList = json.load(json_file)
      else:
        rentedCarsList = []

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

          return f"Car {car} rented successfully for {date.strftime('%Y-%m-%d')}"
      else:
          return f"Car {car} not available for {date.strftime('%Y-%m-%d')}"
    else:
        return f"We do not have the car {car} available for rent"