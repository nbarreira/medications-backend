from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

#from typing import List
#from pydantic import BaseModel

from sql_app.database import get_session
from sql_app.models import Patient, Medication, Posology
from sql_app.utils import create_db_and_tables
from sql_app.crud import *
from sqlmodel import Session


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

# Enable CORS
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


# Create data

@app.post("/patients", status_code=201)
def register_patient(patient: Patient, session: Session = Depends(get_session)):
    registered_patient = create_patient(session, patient)
    if registered_patient is not None:
        return registered_patient
    else:
        raise HTTPException(status_code=409, detail="Patient already exists")
    
@app.post("/patients/{patient_id}/medications")
def add_medication(patient_id: int, medication: Medication, session: Session = Depends(get_session)):
    return create_medication(session, patient_id, medication)

@app.post("/patients/{patient_id}/medications/{medication_id}/posologies")
def add_posology(patient_id: int, medication_id: int, posology: Posology, session: Session = Depends(get_session)):
    return create_posology(session, patient_id, medication_id, posology)


# Retrieve data

@app.get("/patients/{patient_id}")
def get_patient(patient_id: int, session: Session = Depends(get_session)):
    patient = find_patient(session, patient_id=patient_id)
    return patient

@app.get("/patients")
def get_patient_by_username(username: str, session: Session = Depends(get_session)):
    patient = find_patient(session, username=username)
    if patient is not None:
        return patient
    else:
        raise HTTPException(status_code=404, detail="Patient not found")


@app.get("/patients/{patient_id}/medications/{medication_id}")
def get_medication(patient_id: int, medication_id: int, session: Session = Depends(get_session)):
    pass

@app.get("/patients/{patient_id}/medications")
def get_all_medications(patient_id: int, session: Session = Depends(get_session)):
    pass


# Update data

@app.put("/patients/{patient_id}")
def update_patient(patient_id: int, patient: Patient, session: Session = Depends(get_session)):
    pass

@app.put(("/patients/{patient_id}/medications/{medication_id}"))
def update_medication(patient_id: int, medication_id: int, medication: Medication, session: Session = Depends(get_session)):
    pass


# Delete data

@app.delete("/patients/{patient_id}")
def delete_patients(patient_id: int, session: Session = Depends(get_session)):
    delete_patient(session, patient_id)
    return patient_id

@app.delete(("/patients/{patient_id}/medications/{medication_id}"))
def delete_medications(patient_id: int, medication_id: int, session: Session = Depends(get_session)):
    pass

@app.delete(("/patients/{patient_id}/medications/{medication_id}/posologies/{posology_id}"))
def delete_posologies(patient_id: int, medication_id: int, posology_id: int, session: Session = Depends(get_session)):
    pass
