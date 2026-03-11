import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import os

st.set_page_config(page_title="RLHF Apnea Scorer", layout="wide")
st.title("🫁 Clinical Apnea Scorer AI")

# Change this to your EC2 IP when deploying
API_URL = os.getenv("API_URL", "http://localhost:8000/predict_csv")

uploaded_file = st.file_uploader("Upload Patient Data (.csv)", type=["csv"])

if uploaded_file is not None:
    # HARDCODED: Tell pandas there are no headers, then assign them
    df = pd.read_csv(uploaded_file, header=None)
    df.columns = ['PFlow', 'Abdomen', 'Thorax', 'SaO2', 'Vitalog1', 'Vitalog2', 'time_sec']
        
    st.write("### Raw Signal Preview")
    st.dataframe(df.head())
    
    if st.button("Run AI Inference", type="primary"):
        with st.spinner("Segmenting signals and running LSTM model..."):
            
            # Send file to FastAPI
            uploaded_file.seek(0)
            files = {"file": (uploaded_file.name, uploaded_file, "text/csv")}
            response = requests.post(API_URL, files=files)
            
            if response.status_code == 200:
                predictions = response.json().get("predictions", [])
                st.success(f"Analysis complete! Processed {len(predictions)} windows.")
                
                # --- VISUALIZATION ---
                st.write("### Signal Analysis & Apnea Events")
                fig = go.Figure()
                            
                
                # HARDCODED 256 Hz: Allow up to 30 minutes of 256Hz data
                sample_df = df.head(256 * 60 * 30)
                
                # Plot PFlow and SaO2
                fig.add_trace(go.Scatter(x=sample_df['time_sec'], y=sample_df['PFlow'], name="PFlow (Airflow)", opacity=0.8))
                fig.add_trace(go.Scatter(x=sample_df['time_sec'], y=sample_df['SaO2'], name="SaO2 (Oxygen)", opacity=0.8, yaxis="y2"))    
                        
                # Draw Red Rectangles where Apnea is detected
                for pred in predictions:
                    if pred["is_apnea"]:
                        fig.add_vrect(
                            x0=pred["start_time_sec"], 
                            x1=pred["end_time_sec"], 
                            fillcolor="red", opacity=0.3, layer="below", 
                            line_width=0, annotation_text="Apnea Event", annotation_position="top left"
                        )
                
                fig.update_layout(
                    xaxis_title="Time (Seconds)",
                    yaxis_title="Airflow (PFlow)",
                    yaxis2=dict(title="Oxygen Saturation (SaO2)", overlaying="y", side="right"),
                    hovermode="x unified",
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Show raw data
                st.write("### Detailed Window Predictions")
                st.dataframe(pd.DataFrame(predictions))
            else:
                st.error(f"Error from API: {response.text}")