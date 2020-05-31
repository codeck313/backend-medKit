from sqlalchemy.orm import Session

from . import models, schemas
from .models import Patient, MedicalDetails, BedDetails


def get_patient_by_id(db: Session, id: str):
    return db.query(Patient, BedDetails, MedicalDetails).join(BedDetails,
                                                              Patient.patient_id == BedDetails.current_patient_id).join(
        MedicalDetails, Patient.patient_id == MedicalDetails.patient_id).filter(Patient.patient_id == id).first()


def create_user(db: Session, patient: schemas.Patient):
    db_user = models.Patient(patient_id=patient.patient_id, name=patient.name, sex=patient.sex, age=patient.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_all_bed_details(db: Session):
    bed_details = db.query(Patient, BedDetails, MedicalDetails).outerjoin(BedDetails,
                                                                     Patient.patient_id == BedDetails.current_patient_id).outerjoin(
        MedicalDetails, Patient.patient_id == MedicalDetails.patient_id).all()
    return bed_details


def delete_patient_by_id(db: Session, id: str):
    by_id = get_patient_by_id(db, id)
    try:
        db.delete(by_id)
        db.commit()
        return "Patient Deleted Successfully"
    except:
        return "Patient Not Found"
