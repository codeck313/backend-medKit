from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sql import crud, models, schemas
from sql.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post("/patient/create", response_model=schemas.Patient)
def create_patient(patient: schemas.Patient, db: Session = Depends(get_db)):
    print('heeeee')
    db_user = crud.get_patient_by_id(db, id=patient.id)
    if db_user:
        raise HTTPException(status_code=400, detail="Patient already registered")
    return crud.create_user(db=db, patient=patient)


@app.get("/patients/all")
def get_all_patients_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    print("hhhh")
    all_patients = crud.get_all_patients(db, skip=skip, limit=limit)
    res = []
    for patient in all_patients:
        response = schemas.PatientResponse(patient[0], patient[1])
        print(response)
        res.append(response)
    return res


@app.delete("/patients/delete", response_model=str)
def delete_patient(id: str, db: Session = Depends(get_db)):
    all_patients = crud.delete_patient_by_id(db, id)
    return all_patients


@app.get("/patients/{patient_id}", response_model=schemas.Patient, description="Read single patient")
def get_patient_details(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_patient_by_id(db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_user
