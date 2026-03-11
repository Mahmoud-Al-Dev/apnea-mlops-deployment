import torch
import torch.nn as nn
import numpy as np
import pandas as pd
import os

# =================================================================
# 1. THE ARCHITECTURE
# =================================================================
class PentaLSTM(nn.Module):
    def __init__(self, input_size=6, hidden_size=128, num_layers=2):
        super(PentaLSTM, self).__init__()
        self.lstm = nn.LSTM(
            input_size=input_size, 
            hidden_size=hidden_size, 
            num_layers=num_layers, 
            batch_first=True,
            bidirectional=True 
        )
        # Output 3 classes: 0=Normal, 1=CA (Central Apnea), 2=OH (Obstructive Hypopnea)
        self.fc = nn.Linear(hidden_size * 2, 3)

    def forward(self, x):
        # x shape: (Batch, Seq_Len, Features)
        lstm_out, _ = self.lstm(x)
        
        # EXTRACT THE LAST TIMESTEP for window-level classification
        # lstm_out shape: (Batch, Seq_Len, Hidden*2)
        last_timestep = lstm_out[:, -1, :] 
        
        predictions = self.fc(last_timestep) # Shape: (Batch, 3)
        return predictions

# =================================================================
# 2. MODEL LOADER & INFERENCE LOGIC
# =================================================================

MODEL = None
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEIGHTS_PATH = os.path.join(BASE_DIR, "penta_lstm_weights.pth")
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_model():
    """Initializes the model and loads weights from disk."""
    global MODEL
    if MODEL is None:
        MODEL = PentaLSTM().to(DEVICE)
        if os.path.exists(WEIGHTS_PATH):
            MODEL.load_state_dict(torch.load(WEIGHTS_PATH, map_location=DEVICE))
            MODEL.eval()
            print("Model weights loaded successfully.")
        else:
            print(f"WARNING: Weights file {WEIGHTS_PATH} not found. Using random weights.")
    return MODEL

# Initialize model on startup
load_model()

def process_csv_and_predict(df: pd.DataFrame):
    WINDOW_SEC = 30
    
    # 1. DYNAMIC SAMPLING RATE: Calculate the exact Hz from the timestamps
    time_step = df['time_sec'].iloc[1] - df['time_sec'].iloc[0]
    actual_sr = int(round(1 / time_step))
    SAMPLES_PER_WINDOW = actual_sr * WINDOW_SEC
    
    # 2. Extract exactly the 6 features for the LSTM
    FEATURE_COLUMNS = ['PFlow', 'Abdomen', 'Thorax', 'SaO2', 'Vitalog1', 'Vitalog2']
    data = df[FEATURE_COLUMNS].values
    
    # Check for short files
    num_windows = len(data) // SAMPLES_PER_WINDOW
    if num_windows == 0:
        return [] 
        
    # Standardize globally across the whole patient file
    global_mean = np.mean(data, axis=0)
    global_std = np.std(data, axis=0)
    global_std[global_std == 0] = 1  
    data = (data - global_mean) / global_std
    
    windows = []
    
    # Segmenting
    for i in range(num_windows):
        start = i * SAMPLES_PER_WINDOW
        end = start + SAMPLES_PER_WINDOW
        window = data[start:end] 
        windows.append(window)
        
    input_tensor = torch.from_numpy(np.array(windows)).float().to(DEVICE)
    
    # Inference
    with torch.no_grad():
        logits = MODEL(input_tensor)
        
        # NOTE: If you changed back to binary (1 output), use torch.sigmoid here instead!
        probs = torch.softmax(logits, dim=1)
        predicted_classes = torch.argmax(probs, dim=1).cpu().numpy()
    
    # Format Results
    probs_list = probs.cpu().numpy().tolist()
    class_map = {0: "Normal", 1: "Central Apnea", 2: "Obstructive Hypopnea"}
    
    results = []
    for i in range(num_windows):
        class_idx = int(predicted_classes[i])
        
        # 3. REAL TIMESTAMPS: Extract exact time from the dataframe
        start_idx = i * SAMPLES_PER_WINDOW
        end_idx = min((i + 1) * SAMPLES_PER_WINDOW - 1, len(df) - 1)
        
        actual_start_time = float(df['time_sec'].iloc[start_idx])
        actual_end_time = float(df['time_sec'].iloc[end_idx])
        
        results.append({
            "window_index": i,
            "start_time_sec": actual_start_time,  
            "end_time_sec": actual_end_time,      
            "predicted_class": class_map[class_idx],
            "confidence": round(probs_list[i][class_idx], 4),
            "is_apnea": bool(class_idx != 0)
        })
        
    return results