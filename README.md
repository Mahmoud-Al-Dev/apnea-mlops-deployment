# 🫁 Apnea Detection MLOps Pipeline

![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![Ansible](https://img.shields.io/badge/Ansible-EE0000?style=for-the-badge&logo=ansible&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![CI/CD](https://img.shields.io/badge/CI%2FCD-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

📌 Technical Project Overview

This project demonstrates a production-grade MLOps lifecycle for a medical diagnostic tool. It automates the deployment of a FastAPI inference engine that processes 6-channel physiological signals (PFlow, Thorax, Abdomen, Vitalog1, Vitalog2, SaO2) to detect sleep apnea events.

By combining Infrastructure-as-Code (IaC) with Configuration Management, this pipeline ensures that the medical environment is reproducible, secure, and ready for high-performance GPU workloads.

⚙️ CI/CD & Automation Workflow

The project utilizes a decoupled CI/CD pattern to manage infrastructure and software configuration independently:

    Infrastructure Provisioning (Terraform): Defines the "Immutable Infrastructure" layer. It creates a custom VPC, IAM roles with least-privilege ECR access, and security groups that dynamically whitelist the administrator's IP for SSH access.

    Remote State Management (S3): Terraform state is persisted in an AWS S3 bucket with state locking via DynamoDB. This ensures a "Single Source of Truth" and prevents state corruption during concurrent updates.

    Configuration Management (Ansible): Once the hardware is live, Ansible performs OS-level hardening. It bootstraps the NVIDIA Container Toolkit and Docker daemon, ensuring the host is optimized for GPU-accelerated deep learning (PyTorch/LSTM).

    The Glue (Bash Wrapper): A master deploy.sh script orchestrates the handoff between Terraform and Ansible, dynamically injecting ECR registry URLs and EC2 endpoints into the configuration playbooks.

🛠️ Technical Deep Dive

    Signal Processing: The API expects a 2D numpy-compatible array representing multi-channel time-series windows.

    Hardware-Aware Containerization: The Docker image is optimized for a small footprint using python:3.11-slim, but configured via Ansible to leverage host-level NVIDIA runtimes.

    Security & Hardening: * IAM Instance Profiles: The EC2 instance uses temporary credentials via IAM roles to pull images from ECR, eliminating the need for hardcoded AWS keys on the server.

    Network Isolation: The API is isolated within a private/public subnet architecture with strict egress/ingress rules.

## 📂 Repository Structure

```text
apnea-mlops-project/
├── .github/workflows/         # CI/CD pipeline definitions
│   └── ci.yml                 # Automated build and test workflow
├── app/                       # Application & Model source code
│   ├── Dockerfile             # Multi-stage production build
│   ├── main.py                # FastAPI endpoints & validation
│   ├── model.py               # ML Diagnostic logic (RLHF ready)
│   └── requirements.txt       # Python dependencies
├── configuration/             # Ansible playbooks
│   └── playbook.yml           # OS hardening & hardware orchestration
├── infrastructure/            # Terraform IaC definitions
│   ├── main.tf                # VPC, EC2, and IAM resources
│   ├── variables.tf           # Environment configuration
│   ├── outputs.tf             # Deployment state outputs
│   └── providers.tf           # AWS provider & S3 backend config
└── deploy.sh                  # Master orchestration wrapper script
