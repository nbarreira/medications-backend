
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel



class Patient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    name: Optional[str]  = None
    surname: Optional[str] = None
    medications: list["Medication"] = Relationship(back_populates="patient")

class Medication(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    dosage: float = Field(default=1.0)
    start_date: int
    treatment_duration: int = Field(default=1)
    patient_id: int = Field(foreign_key="patient.id")
    patient: Patient = Relationship(back_populates="medications")
    posology: list["Posology"] = Relationship(back_populates="medication")

 
class Posology(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hour: int = Field(primary_key=True)
    minute: int = Field(primary_key=True)
    medication_id: int = Field(foreign_key="medication.id", primary_key=True)
    medication: Medication = Relationship(back_populates="posology")

