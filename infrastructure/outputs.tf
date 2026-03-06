output "api_public_ip" {
  value = aws_instance.api.public_ip
}

output "api_docs_url" {
  value = "http://${aws_instance.api.public_ip}:${var.container_port}/docs"
}
