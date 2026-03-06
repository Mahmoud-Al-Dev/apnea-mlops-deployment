from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from model import predict_apnea
from fastapi import HTTPException
app = FastAPI()

# Define the structure of the incoming data
class SignalData(BaseModel):
    # Expecting a list of lists (the 6-channel time series)
    signals: list[list[float]] 

@app.get("/")
def home():
    return {"message": "Sleep Apnea Detection API is Online"}
@app.get("/health")
def health():
    return {"status": "ok"}
@app.post("/predict")
def get_prediction(data: SignalData):
    # Convert input to numpy for the dummy model
    input_array = np.array(data.signals)
    
    # Basic validation: ensure we have 6 channels
    if input_array.shape[1] != 6:
        raise HTTPException(status_code=400, detail="Input must have exactly 6 channels")


    result = predict_apnea(input_array)
    return result
