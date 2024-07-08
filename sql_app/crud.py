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
    patient_id = kwargs.get('patient_id', None)
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


def find_medications(session: Session, patient_id: int, medication_id: int = None):
    if medication_id is not None:
        statement = select(Medication).where(
            Medication.patient_id == patient_id, 
            Medication.id == medication_id)
        results = session.exec(statement)
        medication = results.first()
        return medication
    else:
        statement = select(Medication).where(
            (Medication.patient_id == patient_id))
        results = session.exec(statement)
        medications = results.all()
        return medications


def find_posologies(session: Session, patient_id: int, medication_id: int):
    statement = select(Medication, Posology).where(Medication.patient_id == patient_id, 
                                                   Medication.id == medication_id, 
                                                   Posology.medication_id == medication_id)
    results = session.exec(statement)
    posologies = []
    for _, posology in results.all():
        posologies.append(posology)
    return posologies


def create_medication(session: Session, medication: Medication):
    try:
        session.add(medication)
        session.commit()
        session.refresh(medication)
        return medication
    except IntegrityError:
        return None


def create_posology(session: Session, posology: Posology):
    try:
        session.add(posology)
        session.commit()
        session.refresh(posology)
        return posology
    except IntegrityError:
        return None


def remove_patient(session: Session, patient_id: int):
    statement = select(Patient).where(Patient.id == patient_id)
    results = session.exec(statement)
    patient = results.first()
    if patient is not None:
        session.delete(patient)
        session.commit()
        return True
    return False


def remove_medication(session: Session, patient_id: int, medication_id: int):
    statement = select(Medication).where(
        Medication.id == medication_id, Medication.patient_id == patient_id)
    results = session.exec(statement)
    patient = results.first()
    if patient is not None:
        session.delete(patient)
        session.commit()
        return True
    return False


def remove_posology(session: Session, patient_id: int, medication_id: int, posology_id: int):
    statement = select(Medication, Posology).where(Medication.id == medication_id, 
                                                   Medication.patient_id == patient_id, 
                                                   Posology.id == posology_id, 
                                                   Posology.medication_id == medication_id)
    results = session.exec(statement)
    data = results.first()
    if data is not None:
        _, posology = data
        session.delete(posology)
        session.commit()
        return True
    return False


def update_patient_data(session: Session, new_patient: Patient):
    patient = find_patient(session, patient_id=new_patient.id)
    if patient is not None:
        patient.name = new_patient.name
        patient.surname = new_patient.surname
        patient.username = new_patient.username
        session.add(patient)
        session.commit()
        session.refresh(patient)
        return True
    return False


def update_medication_data(session: Session, new_medication: Medication):
    medication = find_medications(
        session, patient_id=new_medication.patient_id, medication_id=new_medication.id)
    if medication is not None:
        medication.name = new_medication.name
        medication.dosage = new_medication.dosage
        medication.start_date = new_medication.start_date
        medication.treatment_duration = new_medication.treatment_duration
        session.add(medication)
        session.commit()
        session.refresh(medication)
        return True
    return False
