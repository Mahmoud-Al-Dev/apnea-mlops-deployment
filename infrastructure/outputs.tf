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
