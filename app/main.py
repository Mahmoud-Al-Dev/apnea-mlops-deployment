from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
from model import process_csv_and_predict

app = FastAPI(title="Apnea Detection API")

# Allow Streamlit to talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Replace your predict_csv function in main.py with this:

@app.post("/predict_csv")
async def predict_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
    
    contents = await file.read()
    
    # HARDCODED: Tell pandas there are no headers, then assign them
    df = pd.read_csv(io.BytesIO(contents), header=None)
    df.columns = ['PFlow', 'Abdomen', 'Thorax', 'SaO2', 'Vitalog1', 'Vitalog2', 'time_sec']
    
    try:
        results = process_csv_and_predict(df)
        return {"filename": file.filename, "predictions": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))