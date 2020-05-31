from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship

from .database import Base


class Patient(Base):
    __tablename__ = "patient"
    patient_id = Column(Integer, primary_key=True)
    name = Column(String)
    sex = Column(String)
    age = Column(Integer)
    heart_rate_minima = Column(Float)
    heart_rate_maxima = Column(Float)
    spo2_minima = Column(Float)
    systolic_bp_maxima = Column(Float)
    diastolic_bp_maxima = Column(Float)
    ward_number = Column(String)
    # children = relationship("BedDetails")


class BedDetails(Base):
    __tablename__ = "bedDetails"
    bed_id = Column(Integer, primary_key=True, autoincrement=True)
    bed_no = Column(Integer)
    ward_no = Column(String)
    floor_number = Column(String)
    current_patient_id = Column(Integer, ForeignKey('patient.patient_id'))
    ip_address = Column(String)
    children = relationship("MedicalDetails")


class MedicalDetails(Base):
    __tablename__ = "medicData"
    id = Column(Integer, primary_key=True, autoincrement=True)
    bed_id = Column(Integer, ForeignKey('bedDetails.bed_id'))
    patient_id = Column(Integer, ForeignKey('patient.patient_id'))
    bed_no = Column(Integer)
    time = Column(DateTime)
    temp_current = Column(Float)
    temp_avg = Column(Float)
    bpm_current = Column(Float)
    bpm_avg = Column(Float)
    bp_systolic_current = Column(Float)
    bp_systolic_avg = Column(Float)
    bp_diastolic_current = Column(Float)
    bp_diastolic_avg = Column(Float)
    spo2_current = Column(Float)
    spo2_avg = Column(Float)
