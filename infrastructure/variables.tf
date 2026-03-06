variable "aws_region" {
  type    = string
  default = "eu-central-1"
}

variable "project_name" {
  type    = string
  default = "apnea-api"
}

variable "ecr_repo_name" {
  type    = string
  default = "apnea-api"
}

variable "container_port" {
  type    = number
  default = 8000
}

# Optional: restrict SSH to your public IP/32. Leave "" to disable SSH.
variable "ssh_cidr" {
  type    = string
  default = "" # e.g. "203.0.113.10/32"
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}
