# 🫁 Apnea Detection MLOps Pipeline

![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![Ansible](https://img.shields.io/badge/Ansible-EE0000?style=for-the-badge&logo=ansible&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![HashiCorp Vault](https://img.shields.io/badge/Vault-000000?style=for-the-badge&logo=vault&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![CI/CD](https://img.shields.io/badge/CI%2FCD-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

## 🎯 Final Application Result

<img width="3556" height="1862" alt="Screenshot from 2026-03-11 17-03-55" src="https://github.com/user-attachments/assets/f6b32f32-c79b-48ee-bd0f-38f320c83d35" />

---

## 📌 Technical Project Overview

This project demonstrates a production-grade MLOps lifecycle for a medical diagnostic tool. It automates the deployment of a full-stack AI application featuring a **FastAPI** inference engine and an interactive **Streamlit** frontend, that processes 6-channel physiological signals (PFlow, Thorax, Abdomen, Vitalog1, Vitalog2, SaO2) to detect sleep apnea events.

By combining Infrastructure-as-Code (IaC), zero-trust secrets management, and comprehensive observability, this pipeline ensures that the medical environment is reproducible, highly secure, and dynamically fetches cloud-hosted model artifacts for real-time online analysis.

## ⚙️ CI/CD & Automation Workflow

The project utilizes a decoupled CI/CD pattern to manage infrastructure, software configuration, security, and model artifacts independently:

* **Zero-Trust Secrets Management (HashiCorp Vault):** AWS credentials and sensitive tokens are completely removed from GitHub. The CI/CD pipeline authenticates to an HCP Vault cluster using a machine-identity `AppRole` to dynamically fetch strict, short-lived access keys before provisioning resources.
* **Infrastructure Provisioning (Terraform):** Defines the "Immutable Infrastructure" layer. It automatically inherits the Vault token to provision memory-optimized EC2 instances, custom VPCs, and configures security groups exposing only necessary ports (`8000` for API, `8501` for UI, and `3000` for Grafana).
* **Model Artifact Management (S3):** To prevent Git repository bloat, the heavy PyTorch `.pth` weights are stored in an auto-provisioned AWS S3 bucket. EC2 instances are granted least-privilege IAM roles to read from this bucket.
* **Configuration Management (Ansible):** Once the hardware is live, Ansible performs OS-level hardening, bootstraps the Docker daemon, templates the configuration files, and orchestrates a multi-container Docker Compose stack.
* **The Orchestration Wrapper (Bash):** A master `deploy.sh` script orchestrates the pipeline by dynamically grabbing S3 bucket names and ECR registries from Terraform outputs, securely downloading the model weights into the build context, and triggering the Ansible playbook.

## 🛠️ Technical Deep Dive

* **Enterprise Observability Stack:** The deployment features a fully automated monitoring suite. A **FastAPI Instrumentator** tracks real-time inference latency and request rates, while a **Prometheus Node Exporter** monitors the EC2 host's CPU, RAM, and Disk I/O. **Prometheus** scrapes these metrics every 15 seconds, visualizing them on a secure **Grafana** dashboard deployed alongside the application.
* **Secure Bridge Networking:** The entire application and monitoring stack runs within an isolated Docker Compose bridge network. Prometheus securely scrapes the API and Node Exporter using internal Docker DNS without exposing sensitive metric ports to the public internet.
  <img width="3303" height="1896" alt="Screenshot from 2026-03-18 00-34-49" src="https://github.com/user-attachments/assets/484321f9-08d4-47a0-b0c4-b1f2b82dbac2" />
* **Interactive Medical GUI:** A Streamlit dashboard allows end-users to dynamically upload `.csv` patient data, preview the raw multi-channel signals, and trigger the AI model for online inference.
* **Dynamic Resource Allocation:** The pipeline accounts for the heavy memory overhead of loading large CSVs into Pandas DataFrames and PyTorch Tensors by specifically targeting memory-optimized EC2 instance types to prevent "Out of Memory" hardware crashes.

## 📂 Repository Structure

```text
apnea-mlops-project/
├── .github/workflows/         # CI/CD pipeline definitions
│   └── ci.yml                 # Automated build, Vault Auth, and deploy workflow
├── app/                       # Application & Model source code
│   ├── dashboard.py           # Streamlit UI for dynamic signal upload
│   ├── main.py                # FastAPI backend endpoints with Prometheus instrumentation
│   ├── model.py               # PyTorch ML Diagnostic logic
│   ├── Dockerfile             # Multi-process production container build
│   └── requirements.txt       # Pinned Python dependencies (CPU-optimized)
├── configuration/             # Ansible playbooks and Templating
│   ├── playbook.yml           # OS hardening & Docker Compose orchestration
│   ├── docker-compose.yml.j2  # Jinja2 template for the multi-container stack
│   └── prometheus.yml         # Prometheus scrape configuration targeting API & hardware
├── infrastructure/            # Terraform IaC definitions
│   ├── main.tf                # VPC, EC2, Security Groups, and S3 Bucket
│   ├── variables.tf           # Environment & IP configuration
│   ├── outputs.tf             # Dynamic state outputs (IPs, Bucket names, ECR URLs)
│   └── providers.tf           # AWS & Vault providers with remote state config
├── .dockerignore              # Docker build exclusions
├── .gitignore                 # Git tracking exclusions
└── deploy.sh                  # Master orchestration wrapper script
