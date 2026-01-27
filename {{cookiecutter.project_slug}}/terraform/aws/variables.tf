# ==============================================================================
# Terraform Variables - Customize your deployment
# ==============================================================================

variable "aws_region" {
  description = "AWS region to deploy to"
  type        = string
  default     = "us-east-1"  # TODO: Change to your preferred region
}

variable "app_name" {
  description = "Name of the application"
  type        = string
  default     = "{{ cookiecutter.project_slug }}"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "production"
}

variable "image_tag" {
  description = "Docker image tag to deploy"
  type        = string
  default     = "latest"
}

variable "app_port" {
  description = "Port the application listens on"
  type        = number
  {%- if cookiecutter.ui_framework == 'chainlit' %}
  default     = 8000  # Chainlit default port
  {%- elif cookiecutter.ui_framework == 'streamlit' %}
  default     = 8501  # Streamlit default port
  {%- else %}
  default     = 8080  # Default port
  {%- endif %}
}

variable "cpu" {
  description = "CPU units for the container (1024 = 1 vCPU)"
  type        = string
  default     = "1024"  # TODO: Increase for production (2048, 4096)
}

variable "memory" {
  description = "Memory for the container (2048 = 2GB)"
  type        = string
  default     = "2048"  # TODO: Increase for production (4096, 8192)
}

variable "auto_deploy" {
  description = "Automatically deploy on image push to ECR"
  type        = bool
  default     = true
}

variable "environment_variables" {
  description = "Environment variables for the application"
  type        = map(string)
  default     = {
    MODEL_NAME = "gpt-4o"
    LOG_LEVEL  = "INFO"
  }
  # TODO: Add your custom environment variables here
  # DO NOT add secrets here - use AWS Secrets Manager
}
