from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BasePatient(BaseModel):
    username: str
    name: str
    surname: str

class Patient(BasePatient):
    id: int

class Posology(BaseModel):
    hour: int
    minute: int

class BaseMedicine(BaseModel):
    name: int
    dosage: float
    start_date: int
    treatment_duration: int
    posology: List[Posology]

class Medicine(BaseMedicine):
    id: int


# Create data

@app.post("/patients")
def register_patient(patient: BasePatient):
    pass

@app.post("/patients/{patient_id}/medicines")
def add_medicine(patient_id: int, medicine: BaseMedicine):
    pass


# Retrieve data

@app.get("/patients/{patient_id}")
def get_patient(patient_id: int):
    pass

@app.get("/patients")
def get_patient_by_username(username: str):
    pass

@app.get("/patients/{patient_id}/medicines/{medicine_id}")
def get_medicine(patient_id: int, medicine_id: int):
    pass

@app.get("/patients/{patient_id}/medicines")
def get_all_medicines(patient_id: int):
    pass


# Update data

@app.put("/patients/{patient_id}")
def update_patient(patient_id: int, patient: BasePatient):
    pass

@app.put(("/patients/{patient_id}/medicines/{medicine_id}"))
def update_medicine(patient_id: int, medicine_id: int, medicine: BaseMedicine):
    pass


# Delete data

@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):
    pass

@app.delete(("/patients/{patient_id}/medicines/{medicine_id}"))
def delete_medicine(patient_id: int, medicine_id: int):
    pass
