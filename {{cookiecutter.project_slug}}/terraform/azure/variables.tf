# ==============================================================================
# Terraform Variables for Azure - Customize your deployment
# ==============================================================================

variable "location" {
  description = "Azure region to deploy to"
  type        = string
  default     = "westeurope"  # TODO: Change to your preferred region
}

variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
  default     = "{{ cookiecutter.project_slug }}-rg"
}

variable "app_name" {
  description = "Name of the application"
  type        = string
  default     = "{{ cookiecutter.project_slug }}"
}

variable "acr_name" {
  description = "Name of the Azure Container Registry (must be globally unique)"
  type        = string
  default     = "{{ cookiecutter.project_slug | replace('-', '') }}acr"  # ACR names can't have dashes
}

variable "acr_sku" {
  description = "SKU for Azure Container Registry"
  type        = string
  default     = "Basic"  # Options: Basic, Standard, Premium
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
  description = "CPU cores for the container (0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0)"
  type        = number
  default     = 0.5  # TODO: Increase for production (1.0, 2.0)
}

variable "memory" {
  description = "Memory for the container in GB (0.5Gi, 1.0Gi, 1.5Gi, 2.0Gi, etc.)"
  type        = string
  default     = "1.0Gi"  # TODO: Increase for production (2.0Gi, 4.0Gi)
}

variable "min_replicas" {
  description = "Minimum number of container replicas"
  type        = number
  default     = 1  # TODO: Increase for HA (2+)
}

variable "max_replicas" {
  description = "Maximum number of container replicas"
  type        = number
  default     = 3  # TODO: Adjust based on expected load
}

variable "environment_variables" {
  description = "Environment variables for the application"
  type        = map(string)
  default     = {
    MODEL_NAME = "gpt-4o"
    LOG_LEVEL  = "INFO"
  }
  # TODO: Add your custom environment variables here
  # DO NOT add secrets here - use Azure Key Vault
}

# Optional: Secrets from Azure Key Vault
# variable "openai_api_key" {
#   description = "OpenAI API Key (from Key Vault or GitHub Secrets)"
#   type        = string
#   sensitive   = true
# }
