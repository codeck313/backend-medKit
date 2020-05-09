from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Patient(Base):
    __tablename__ = "patient"

    id = Column(Integer, primary_key=True, index=True)
    Name = Column(String)
    BedNo = Column(Integer)
    Sex = Column(String)
    Age = Column(Integer)
