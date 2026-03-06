# 🫁 Apnea Detection MLOps Pipeline

![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![Ansible](https://img.shields.io/badge/Ansible-EE0000?style=for-the-badge&logo=ansible&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)

## 📌 Project Overview
This repository contains a fully automated **Infrastructure-as-Code (IaC)** and **Configuration Management** pipeline designed to deploy a Medical AI application. 

Currently, it serves a high-performance FastAPI endpoint that processes 6-channel time-series data to detect Sleep Apnea. This infrastructure lays the foundation for migrating from a baseline dummy model to a production-ready **RLHF (Reinforcement Learning from Human Feedback)** loop for medical diagnostics.

## 🏗️ Architecture

The deployment is decoupled into two distinct phases for professional state management:

1. **The Architect (Terraform):** Provisions the AWS VPC, public subnets, internet gateways, dynamic security groups, IAM roles for ECR access, and an EC2 instance.
2. **The Decorator (Ansible):** Connects via SSH to secure the OS, install the Docker daemon, bootstrap the **NVIDIA Container Toolkit** (for future GPU acceleration), and pull/run the inference container from AWS ECR.

## 📂 Repository Structure

```text
apnea-mlops-project/
├── README.md                  # Project documentation
│
├── app/                       # Application & Model source code
│   ├── Dockerfile             # Multi-stage build for the FastAPI inference server
│   ├── main.py                # API endpoints and data validation
│   ├── model.py               # Dummy diagnostic logic (preparing for RLHF model)
│   └── requirements.txt       
│
├── infrastructure/            # Terraform IaC definitions
│   ├── main.tf                # VPC, EC2, IAM, and Security Group provisioning
│   ├── variables.tf           # Environment configuration
│   ├── outputs.tf             # IP and URL state outputs
│   └── providers.tf           # AWS provider configuration
│
└── configuration/             # Ansible Configuration Management
    └── playbook.yml           # OS hardening, Docker, and NVIDIA toolkit setup
