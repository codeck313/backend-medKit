from sqlalchemy.orm import Session

from . import models, schemas
from .models import Patient, MedicalDetails, BedDetails


def get_patient_by_id(db: Session, id: str):
    return db.query(models.Patient).filter(models.Patient.patient_id == id).first()


def get_all_patients(db: Session, skip: int = 0, limit: int = 100):
    details = db.query(models.Patient, models.MedicalDetails).filter(
        models.Patient.patient_id == models.MedicalDetails.id).offset(skip).limit(limit).all()
    print("Fetched....")
    print(len(details))
    for r in details:
        print(r)
    return details


def create_user(db: Session, patient: schemas.Patient):
    db_user = models.Patient(id=patient.id, Name=patient.Name, BedNo=patient.BedNo, Sex=patient.Sex,
                             Age=patient.Age)
    print("here")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_all_bed_details(db: Session):
    bed_details = db.query(Patient, BedDetails, MedicalDetails).join(BedDetails,
                                                                     Patient.patient_id == BedDetails.current_patient_id).join(
        MedicalDetails, Patient.patient_id == MedicalDetails.patient_id).all()
    print(len(bed_details))
    print(bed_details[0])
    return bed_details

def delete_patient_by_id(db: Session, id: str):
    by_id = get_patient_by_id(db, id)
    try:
        db.delete(by_id)
        db.commit()
        return "Patient Deleted Successfully"
    except:
        return "Patient Not Found"
