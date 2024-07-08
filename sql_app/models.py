
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from pydantic import BaseModel

class Message(BaseModel):
    detail: str

class Patient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    name: Optional[str]  = None
    surname: Optional[str] = None
    medications: list["Medication"] = Relationship(back_populates="patient", sa_relationship_kwargs={"cascade": "delete"})

class Medication(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    dosage: float = Field(default=1.0)
    start_date: str
    treatment_duration: int = Field(default=1)
    patient_id: int = Field(foreign_key="patient.id")
    patient: Patient = Relationship(back_populates="medications")
    posology: list["Posology"] = Relationship(back_populates="medication", sa_relationship_kwargs={"cascade": "delete"})

 
class Posology(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hour: int
    minute: int
    medication_id: int = Field(foreign_key="medication.id")
    medication: Medication = Relationship(back_populates="posology")
    intakes: list["Intake"] = Relationship(back_populates="posology", sa_relationship_kwargs={"cascade": "delete"})


class Intake(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: str
    posology_id: int = Field(foreign_key="posology.id")
    posology: Posology = Relationship(back_populates="intakes")
