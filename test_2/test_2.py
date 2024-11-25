from fastapi import FastAPI
from datetime import date

app = FastAPI()

@app.get("/dateAvaiblesCars")
def dateAvaiablesCars(date: date):
    return 

@app.post("/rentCar")
def rentCar(car: str, date: date):
    return