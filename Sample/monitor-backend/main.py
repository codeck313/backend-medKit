from typing import List

from fastapi import Depends, FastAPI, HTTPException, WebSocket
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session
from sql import crud, models, schemas, response
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


@app.post("/patient/create", response_model=schemas.Patient, description="Create a new patient")
def create_patient(patient: schemas.Patient, db: Session = Depends(get_db)):
    db_user = crud.get_patient_by_id(db, id=patient.patient_id)
    if db_user:
        raise HTTPException(status_code=400, detail="Patient already registered")
    return crud.create_user(db=db, patient=patient)


@app.delete("/patients/delete", response_model=str)
def delete_patient(id: str, db: Session = Depends(get_db)):
    all_patients = crud.delete_patient_by_id(db, id)
    return all_patients


@app.get("/patients/{patient_id}", description="Read single patient")
def get_patient_details(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_patient_by_id(db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return response.BedResponse(db_user[0], db_user[1], db_user[2])


@app.get("/beds/all", description="Get All Beds")
def get_patient_details(db: Session = Depends(get_db)):
    all_beds_details = crud.get_all_bed_details(db)
    if all_beds_details is None:
        raise HTTPException(status_code=404, detail="No Beds found")
    details = []
    for bed in all_beds_details:
        details.append(response.BedResponse(bed[0], bed[1], bed[2]))
    return details


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
