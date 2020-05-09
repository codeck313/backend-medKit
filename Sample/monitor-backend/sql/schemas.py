from pydantic import BaseModel


class Patient(BaseModel):
    id: int
    Name: str
    BedNo: int
    Age: int
    Sex: str

    class Config:
        orm_mode = True
