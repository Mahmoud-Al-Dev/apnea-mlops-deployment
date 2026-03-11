FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
EXPOSE 8501

# Create a start script
RUN echo "#!/bin/bash\nuvicorn main:app --host 0.0.0.0 --port 8000 & \nstreamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0" > start.sh
RUN chmod +x start.sh

CMD ["./start.sh"]