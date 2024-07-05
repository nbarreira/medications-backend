from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from .database import engine
from .models import Patient, Medication, Posology


def create_patient(session: Session, patient: Patient):
    statement = select(Patient).where(Patient.username == patient.username)
    results = session.exec(statement)
    registered_patient = results.first()
    if registered_patient is None:
        session.add(patient)
        session.commit()
        session.refresh(patient)
        return patient
    else:
        return None


def find_patient(session: Session, **kwargs):
    patient_id = kwargs.get('patientId', None)
    username = kwargs.get('username', None)
    if patient_id:
        statement = select(Patient).where(Patient.id == patient_id)
        results = session.exec(statement)
        patient = results.first()
        return patient
    if username:
        statement = select(Patient).where(Patient.username == username)
        results = session.exec(statement)
        patient = results.first()
        return patient
    return None

def create_medication(session: Session, patient_id: int, medication: Medication):
    try:
        session.add(medication)
        session.commit()
        session.refresh(medication)
        return medication
    except IntegrityError:
        pass
    return None
    

def create_posology(session: Session, patient_id: int, medication_id: int, posology: Posology):
    session.add(posology)
    session.commit()
    session.refresh(posology)
    return posology

def delete_patient(session:Session, patient_id: int):
    print("borrando", patient_id)
    statement = select(Patient).where(Patient.id == patient_id)
    results = session.exec(statement)
    patient = results.first()
    session.delete(patient)
    session.commit()
