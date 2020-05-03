from pydantic import BaseModel


class Patient(BaseModel):
    id: str
    name: str
    bedNumber: str
    age: int
    sex: str

    class Config:
        orm_mode = True
