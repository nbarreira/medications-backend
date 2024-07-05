from .database import engine
from .models import Patient, Medication, Posology
from sqlmodel import SQLModel, text, Session


def create_db_and_tables():  
    SQLModel.metadata.create_all(engine) 
    # Foreign keys are disabled in sqlite3 by default
    with Session(engine) as session:
        session.exec(text("PRAGMA foreign_keys = ON"))
 
