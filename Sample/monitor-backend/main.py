from typing import List

from fastapi import Depends, FastAPI, HTTPException, WebSocket
from fastapi.responses import Response
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from sql import crud, models, schemas, response
from sql.database import SessionLocal, engine
import random
import traceback

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        traceback.print_exc()
        return Response("Internal server error", status_code=500)


app.middleware('http')(catch_exceptions_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# @app.post("/patient/create", response_model=schemas.Patient, description="Create a new patient")
# def create_patient(patient: schemas.Patient, db: Session = Depends(get_db)):
#     db_user = crud.get_patient_by_id(db, id=patient.patient_id)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Patient already registered")
#     return crud.create_user(db=db, patient=patient)
#

@app.delete("/patients/delete", response_model=str)
def delete_patient(id: str, db: Session = Depends(get_db)):
    all_patients = crud.delete_patient_by_id(db, id)
    return all_patients


@app.get("/beds/{bed_id}", description="Get Details of a Bed")
def get_bed_details(bed_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_bed_details_by_id(db, bed_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return response.BedResponse(db_user[0], db_user[1], db_user[2])


@app.get("/beds", description="Get All Beds")
def get_all_bed_details(floor_number: str = None, ward_number: str = None, db: Session = Depends(get_db)):
    all_beds_details = crud.get_all_bed_details(db, ward_number, floor_number)
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
