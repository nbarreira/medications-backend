#!/usr/bin/python3

from typing import Optional
from sqlmodel import Field, Session, Relationship, SQLModel, create_engine

import sys

sqlite_file_name = "medicines.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

class Patient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    name: Optional[str]  = None
    surname: Optional[str] = None
    medicines: list["Medicine"] = Relationship(back_populates="medicine")

class Medicine(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    dosage: float = Field(default=1.0)
    start_date: int
    treatment_duration: int = Field(default=1)
    patient_id: int = Field(foreign_key="patient.id")
    posology: list["Posology"] = Relationship(back_populates="posology")

class Posology(SQLModel, table=True):
    hour: int = Field(primary_key=True)
    minute: int = Field(primary_key=True)
    medicine_id: int = Field(foreign_key="medicine.id", primary_key=True)



def create_db_and_tables():  
    SQLModel.metadata.create_all(engine)  

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} --init")
        sys.exit()
    engine = create_engine(sqlite_url, echo=True)

    if sys.argv[1] == "--init":
        create_db_and_tables()