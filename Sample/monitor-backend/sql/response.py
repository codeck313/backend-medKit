from .models import Patient, MedicalDetails, BedDetails


class BedResponse:
    id: int
    name: str
    age: int
    sex: str
    floor_number: str
    bed_no: str
    ip_address: str
    ward_no: str
    bed_id: str
    time: str
    tempCurrent = float
    tempAvg = float
    bpmCurrent = float
    bpmAvg = float
    bpCurrent = float
    bpAvg = float
    spO2Current = float
    spO2Avg = float

    def __init__(self, patient_details: Patient, bed_details: BedDetails, medical_details: MedicalDetails):
        self.id = patient_details.patient_id
        self.name = patient_details.name
        self.age = patient_details.age
        self.sex = patient_details.sex
        self.floor_number = bed_details.floor_number
        self.bed_no = bed_details.floor_number
        self.ip_address = bed_details.ip_address
        self.ward_no = bed_details.ward_no
        self.bed_id = str(bed_details.bed_id)
        self.time = str(medical_details.time)
        self.tempCurrent = medical_details.tempCurrent
        self.tempAvg = medical_details.tempAvg
        self.bpmCurrent = medical_details.bpmCurrent
        self.bpmAvg = medical_details.bpmAvg
        self.bpCurrent = medical_details.bpCurrent
        self.bpAvg = medical_details.bpmAvg
        self.spO2Current = medical_details.spO2Current
        self.spO2Avg = medical_details.spO2Avg
