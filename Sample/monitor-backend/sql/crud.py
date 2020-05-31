from sqlalchemy.orm import Session

from . import models, schemas
from .models import Patient, MedicalDetails, BedDetails


def get_bed_details_by_id(db: Session, bed_id: str):
    return db.query(BedDetails, Patient, MedicalDetails).join(Patient,
                                                              Patient.patient_id == BedDetails.current_patient_id).join(
        MedicalDetails, BedDetails.current_patient_id == MedicalDetails.patient_id).filter(
        BedDetails.bed_id == bed_id).first()


# def create_user(db: Session, patient: schemas.Patient):
#     db_user = models.Patient(patient_id=patient.patient_id, name=patient.name, sex=patient.sex, age=patient.age)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


def get_all_bed_details(db: Session, ward_number: str, floor_number: str):
    bed_details = db.query(BedDetails, Patient, MedicalDetails).join(Patient,
                                                                     Patient.patient_id == BedDetails.current_patient_id).join(
        MedicalDetails, BedDetails.current_patient_id == MedicalDetails.patient_id).filter(
        BedDetails.ward_no == ward_number).filter(BedDetails.floor_number == floor_number).all()
    return bed_details


def delete_patient_by_id(db: Session, id: str):
    by_id = get_bed_details_by_id(db, id)
    try:
        db.delete(by_id)
        db.commit()
        return "Patient Deleted Successfully"
    except:
        return "Patient Not Found"
