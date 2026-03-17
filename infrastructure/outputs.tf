output "api_public_ip" {
  value = aws_instance.api.public_ip
}

output "api_docs_url" {
  value = "http://${aws_instance.api.public_ip}:${var.container_port}/docs"
}

output "weights_bucket_name" {
  value       = aws_s3_bucket.ml_weights.id
  description = "The name of the S3 bucket created for ML weights"
}

output "ecr_registry_url" {
  value       = local.ecr_registry
  description = "The URL of the AWS ECR registry"
}

output "ecr_image_url" {
  value       = local.ecr_image
  description = "The full URL of the ECR image including the latest tag"
}