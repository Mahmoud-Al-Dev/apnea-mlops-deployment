#!/bin/bash
set -e 

echo "🔍 Fetching infrastructure details..."

# 1. Grab the IP from Terraform (Using -chdir to tell Terraform where the files are)
EC2_IP=$(terraform -chdir=infrastructure output -raw api_public_ip)

# 2. Grab ECR variables directly from Terraform outputs!
ECR_REGISTRY=$(terraform -chdir=infrastructure output -raw ecr_registry_url)
ECR_IMAGE=$(terraform -chdir=infrastructure output -raw ecr_image_url)

# 3. Dynamically grab the S3 Bucket Name from Terraform outputs
S3_BUCKET_NAME=$(terraform -chdir=infrastructure output -raw weights_bucket_name)

echo "----------------------------------------"
echo "🚀 Target EC2 IP: $EC2_IP"
echo "📦 ECR Registry:  $ECR_REGISTRY"
echo "🪣 ML Bucket:     $S3_BUCKET_NAME"
echo "----------------------------------------"

# 4. Download the weights from S3 into the app folder BEFORE building Docker
echo "⬇️ Downloading model weights from S3..."
aws s3 cp s3://${S3_BUCKET_NAME}/penta_lstm_weights.pth ./app/

# 5. Run Ansible (Pointing it to the playbook inside the configuration folder)
ansible-playbook -i "$EC2_IP," configuration/playbook.yml \
  --user ubuntu \
  --private-key ~/.ssh/apnea_key \
  --extra-vars "ecr_registry_url=$ECR_REGISTRY ecr_image_url=$ECR_IMAGE"

echo "✅ Deployment Complete!"