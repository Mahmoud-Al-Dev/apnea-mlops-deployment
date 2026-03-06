import numpy as np

def predict_apnea(input_data):
    """
    input_data: A 2D array of shape (time_steps, 6)
    Mimics your 6 channels: PFlow, Thorax, Abdomen, Vitalog1, Vitalog2, SaO2
    """
    # Simulate a 'Penta-LSTM' processing the window
    # In a real model, this would be: model.predict(input_data)
    
    # Dummy logic: If PFlow (index 0) is low and SaO2 (index 5) is dipping, return high probability
    pflow_avg = np.mean(input_data[:, 0])
    sao2_avg = np.mean(input_data[:, 5])
    
    if pflow_avg < 0.3 and sao2_avg < 0.90:
        return {"probability": 0.88, "status": "Apnea Detected"}
    return {"probability": 0.12, "status": "Normal Breathing"}