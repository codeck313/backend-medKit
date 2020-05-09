from typing import List

from fastapi import Depends, FastAPI, HTTPException, WebSocket
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session

from sql import crud, models, schemas
from sql.database import SessionLocal, engine
import random

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


def generate_random():
    return [round(random.uniform(30, 150), 2), round(random.uniform(30, 150), 2)]


def generate_sample_data():
    return {'123458': {'temp': generate_random(), 'heartRate': generate_random(), 'SpO2': generate_random(),
                       'BP': generate_random()}}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("connected")
    while True:
        print("here")
        data = await websocket.receive_text()
        print(data)
        await websocket.send_json(generate_sample_data())
