# 🫁 Apnea Detection MLOps Pipeline

![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![Ansible](https://img.shields.io/badge/Ansible-EE0000?style=for-the-badge&logo=ansible&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![CI/CD](https://img.shields.io/badge/CI%2FCD-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

## 🎯 Final Application Result

<img width="3556" height="1862" alt="Screenshot from 2026-03-11 17-03-55" src="https://github.com/user-attachments/assets/f6b32f32-c79b-48ee-bd0f-38f320c83d35" />


---

## 📌 Technical Project Overview

This project demonstrates a production-grade MLOps lifecycle for a medical diagnostic tool. It automates the deployment of a full-stack AI application featuring a **FastAPI** inference engine and an interactive **Streamlit** frontend, that processes 6-channel physiological signals (PFlow, Thorax, Abdomen, Vitalog1, Vitalog2, SaO2) to detect sleep apnea events.

By combining Infrastructure-as-Code (IaC) with Configuration Management, this pipeline ensures that the medical environment is reproducible, secure, and dynamically fetches cloud-hosted model artifacts for real-time online analysis.

## ⚙️ CI/CD & Automation Workflow

The project utilizes a decoupled CI/CD pattern to manage infrastructure, software configuration, and model artifacts independently:

* **Infrastructure Provisioning (Terraform):** Defines the "Immutable Infrastructure" layer. It creates a custom VPC, provisions memory-optimized EC2 instances, and configures security groups that explicitly expose ports for the API (`8000`) and the UI (`8501`).
* **Model Artifact Management (S3):** To prevent Git repository bloat, the heavy PyTorch `.pth` weights are stored in an auto-provisioned AWS S3 bucket. EC2 instances are granted least-privilege IAM roles to read from this bucket.
* **Configuration Management (Ansible):** Once the hardware is live, Ansible performs OS-level hardening, bootstraps the Docker daemon, and pulls the latest multi-service container from AWS ECR.
* **The Orchestration Wrapper (Bash):** A master `deploy.sh` script orchestrates the pipeline by dynamically grabbing the S3 bucket name from Terraform outputs, securely downloading the model weights into the build context, and triggering the Ansible playbook.

## 🛠️ Technical Deep Dive

* **Interactive Medical GUI:** A Streamlit dashboard allows end-users to dynamically upload `.csv` patient data, preview the raw multi-channel signals, and trigger the AI model for online inference.
* **Dual-Process Containerization:** The application uses a specialized `Dockerfile` that executes both the FastAPI backend and Streamlit frontend concurrently using module execution (`python -m`), completely isolated within a `python:3.11-slim` environment.
* **Dynamic Resource Allocation:** The pipeline accounts for the heavy memory overhead of loading large CSVs into Pandas DataFrames and PyTorch Tensors by specifically targeting memory-optimized EC2 instance types to prevent "Out of Memory" hardware crashes.

## 📂 Repository Structure

```text
apnea-mlops-project/
├── .github/workflows/         # CI/CD pipeline definitions
│   └── ci.yml                 # Automated build and deploy workflow
├── app/                       # Application & Model source code
│   ├── dashboard.py           # Streamlit UI for dynamic signal upload
│   ├── main.py                # FastAPI backend endpoints & validation
│   ├── model.py               # PyTorch ML Diagnostic logic
│   ├── Dockerfile             # Multi-process production container build
│   └── requirements.txt       # Pinned Python dependencies (CPU-optimized)
├── configuration/             # Ansible playbooks
│   └── playbook.yml           # OS hardening & Docker orchestration
├── infrastructure/            # Terraform IaC definitions
│   ├── main.tf                # VPC, EC2, Security Groups, and S3 Bucket
│   ├── variables.tf           # Environment & IP configuration
│   ├── outputs.tf             # Dynamic state outputs (IPs, Bucket names)
│   └── providers.tf           # AWS provider & Remote state config
├── .dockerignore              # Docker build exclusions
├── .gitignore                 # Git tracking exclusions
└── deploy.sh                  # Master orchestration wrapper script
