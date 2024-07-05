from .database import engine
from .models import Patient, Medication, Posology
from sqlmodel import SQLModel


def create_db_and_tables():  
    SQLModel.metadata.create_all(engine)  

if __name__ == "__main__":
    create_db_and_tables()