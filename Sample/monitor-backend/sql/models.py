from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship

from .database import Base


class Patient(Base):
    __tablename__ = "patient"

    id = Column(Integer, primary_key=True, index=True)
    Name = Column(String)
    BedNo = Column(Integer)
    Sex = Column(String)
    Age = Column(Integer)


class PatientDetails(Base):
    __tablename__ = "medicData"

    id = Column(Integer,primary_key=True)
    Time = Column(DateTime)
    tempCurrent = Column(Float)
    tempAvg = Column(Float)
    bpmCurrent = Column(Float)
    bpmAvg = Column(Float)
    bpCurrent = Column(Float)
    bpAvg = Column(Float)
    spO2Current = Column(Float)
    spO2Avg = Column(Float)
