from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import datetime

from sql_app.database import get_session
from sql_app.models import Patient, Medication, Posology, Message
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

@app.post("/patients",
          status_code=201,
          responses={201: {"model": Patient}, 409: {"model": Message}})
def register_patient(patient: Patient, session: Session = Depends(get_session)):
    registered_patient = create_patient(session, patient)
    if registered_patient is not None:
        return registered_patient
    else:
        raise HTTPException(status_code=409, detail="Patient already exists")


@app.post("/patients/{patient_id}/medications",
          status_code=201,
          responses={201: {"model": Medication}, 422: {"model": Message}})
def add_medication(patient_id: int, medication: Medication, session: Session = Depends(get_session)):
    try:
        date = datetime.datetime.strptime(medication.start_date, "%Y-%m-%d")
        medication.patient_id = patient_id
        new_medication = create_medication(session, medication)
        if new_medication is not None:
            return new_medication
    except ValueError:
        pass
    raise HTTPException(
        status_code=422, detail=f"Medication {medication} could not be inserted: invalid data")


@app.post("/patients/{patient_id}/medications/{medication_id}/posologies",
          status_code=201,
          responses={201: {"model": Posology}, 422: {"model": Message}})
def add_posology(patient_id: int, medication_id: int, posology: Posology, session: Session = Depends(get_session)):
    if posology.hour >= 0 and posology.hour < 24 and posology.minute >= 0 and posology.minute < 60:
        posology.medication_id = medication_id
        medication = find_medications(session, patient_id, medication_id)
        if medication is not None:
            new_posology = create_posology(session, posology)
            if new_posology is not None:
                return new_posology
    raise HTTPException(
        status_code=422, detail=f"Posology {posology} could not be inserted into medication {medication_id} and patient {patient_id}: invalid data")


# Retrieve data
@app.get("/patients/{patient_id}",
         responses={200: {"model": Patient}, 404: {"model": Message}})
def get_patient(patient_id: int, session: Session = Depends(get_session)):
    patient = find_patient(session, patient_id=patient_id)
    if patient is not None:
        return patient
    else:
        raise HTTPException(status_code=404, detail="Patient not found")


@app.get("/patients",
         responses={200: {"model": Patient}, 404: {"model": Message}})
def get_patient_by_username(username: str, session: Session = Depends(get_session)):
    patient = find_patient(session, username=username)
    if patient is not None:
        return patient
    else:
        raise HTTPException(status_code=404, detail="Patient not found")


@app.get("/patients/{patient_id}/medications/{medication_id}",
         responses={200: {"model": Medication}, 404: {"model": Message}})
def get_medication(patient_id: int, medication_id: int, session: Session = Depends(get_session)):
    medication = find_medications(session, patient_id, medication_id)
    if medication is not None:
        return medication
    else:
        raise HTTPException(status_code=404, detail="Medication not found")


@app.get("/patients/{patient_id}/medications",
         responses={200: {"model": list[Medication]}, 404: {"model": Message}})
def get_all_medications(patient_id: int, session: Session = Depends(get_session)):
    medications = find_medications(session, patient_id)
    if len(medications) > 0:
        return medications
    raise HTTPException(
        status_code=404, detail=f"Medications for {patient_id} not found")


@app.get("/patients/{patient_id}/medications/{medication_id}/posologies",
         responses={200: {"model": list[Posology]}, 404: {"model": Message}})
def get_posologies(patient_id: int, medication_id: int, session: Session = Depends(get_session)):
    posologies = find_posologies(session, patient_id, medication_id)
    if len(posologies) > 0:
        return posologies
    raise HTTPException(
        status_code=404, detail=f"Posologies for {patient_id} and medication {medication_id} not found")


# Update data

@app.patch("/patients/{patient_id}",
           status_code=204,
           responses={404: {"model": Message}})
def update_patient(patient_id: int, patient: Patient, session: Session = Depends(get_session)):
    patient.id = patient_id
    if not update_patient_data(session, patient):
        raise HTTPException(
            status_code=404, detail=f"Patient {patient_id} could not be updated")


@app.patch(("/patients/{patient_id}/medications/{medication_id}"),
           status_code=204,
           responses={404: {"model": Message}})
def update_medication(patient_id: int, medication_id: int, medication: Medication, session: Session = Depends(get_session)):
    medication.id = medication_id
    medication.patient_id = patient_id
    if not update_medication_data(session, medication):
        raise HTTPException(
            status_code=404, detail=f"Medication {medication_id} for patient {patient_id} could not be updated")


# Delete data
@app.delete("/patients/{patient_id}",
            status_code=204,
            responses={404: {"model": Message}})
def delete_patients(patient_id: int, session: Session = Depends(get_session)):
    if not remove_patient(session, patient_id):
        raise HTTPException(
            status_code=404, detail=f"Patient {patient_id} not found")


@app.delete(("/patients/{patient_id}/medications/{medication_id}"),
            status_code=204,
            responses={404: {"model": Message}})
def delete_medications(patient_id: int, medication_id: int, session: Session = Depends(get_session)):
    if not remove_medication(session, patient_id, medication_id):
        raise HTTPException(
            status_code=404, detail=f"Medication {medication_id} not found for patient {patient_id}")


@app.delete(("/patients/{patient_id}/medications/{medication_id}/posologies/{posology_id}"),
            status_code=204,
            responses={404: {"model": Message}})
def delete_posologies(patient_id: int, medication_id: int, posology_id: int, session: Session = Depends(get_session)):
    if not remove_posology(session, patient_id, medication_id, posology_id):
        raise HTTPException(
            status_code=404, detail=f"Posology {posology_id} not found for patient {patient_id} and medication {medication_id}")
