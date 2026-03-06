terraform {
  required_version = ">= 1.5.0"

  backend "s3" {
    bucket         = "apnea-mlops-state-mahmoud123321" # Use the exact name from Step 1
    key            = "terraform.tfstate"         # The name of the file inside the bucket
    region         = "eu-central-1"
    encrypt        = true                        # AES-256 encryption at rest
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}
