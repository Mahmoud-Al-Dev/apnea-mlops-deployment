#!/bin/bash
set -e 

echo "🔍 Fetching infrastructure details..."

# 1. Grab the IP from Terraform (Using -chdir to tell Terraform where the files are)
EC2_IP=$(terraform -chdir=infrastructure output -raw api_public_ip)

# 2. Grab your AWS Account ID dynamically using the AWS CLI
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION="eu-central-1"

# 3. Construct the ECR variables
ECR_REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com"
ECR_IMAGE="${ECR_REGISTRY}/apnea-api:latest"

echo "----------------------------------------"
echo "🚀 Target EC2 IP: $EC2_IP"
echo "📦 ECR Registry:  $ECR_REGISTRY"
echo "----------------------------------------"
echo "⚙️  Starting Ansible Playbook..."

# 4. Run Ansible (Pointing it to the playbook inside the configuration folder)
ansible-playbook -i "$EC2_IP," configuration/playbook.yml \
  --user ubuntu \
  --private-key ~/.ssh/apnea_key \
  --extra-vars "ecr_registry_url=$ECR_REGISTRY ecr_image_url=$ECR_IMAGE"

echo "✅ Deployment Complete!"
