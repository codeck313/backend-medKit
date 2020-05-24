from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship

from .database import Base


class Patient(Base):
    __tablename__ = "patient"
    patient_id = Column(Integer, primary_key=True)
    name = Column(String)
    sex = Column(String)
    age = Column(Integer)
    children = relationship("BedDetails")



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
    tempCurrent = Column(Float)
    tempAvg = Column(Float)
    bpmCurrent = Column(Float)
    bpmAvg = Column(Float)
    bpCurrent = Column(Float)
    bpAvg = Column(Float)
    spO2Current = Column(Float)
    spO2Avg = Column(Float)

