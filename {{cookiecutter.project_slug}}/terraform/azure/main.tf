# ==============================================================================
# Azure Container Apps Deployment - Terraform
# ==============================================================================
#
# 🎯 PHILOSOPHY: "Single Source of Truth across clouds"
#
# This Terraform config deploys your Docker container to Azure Container Apps.
# Unified syntax with AWS deployment = easier to maintain!
#
# 🚀 CUSTOMIZATION: Everything here is a starting point. Adjust as needed!
# - Add Azure Database for PostgreSQL
# - Add Azure CDN
# - Add custom domains
# - Add Azure Key Vault for secrets
#
# ==============================================================================

terraform {
  required_version = ">= 1.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }

  # TODO: Configure remote state (Azure Storage)
  # backend "azurerm" {
  #   resource_group_name  = "terraform-state-rg"
  #   storage_account_name = "tfstate"
  #   container_name       = "tfstate"
  #   key                  = "{{ cookiecutter.project_slug }}.tfstate"
  # }
}

provider "azurerm" {
  features {}
}

# ==============================================================================
# Resource Group - Container for all Azure resources
# ==============================================================================

resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location

  tags = {
    Project     = "{{ cookiecutter.project_name }}"
    ManagedBy   = "Terraform"
    Environment = var.environment
  }
}

# ==============================================================================
# Container Registry (ACR) - Where your Docker images live
# ==============================================================================

resource "azurerm_container_registry" "acr" {
  name                = var.acr_name
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = var.acr_sku  # Basic, Standard, or Premium
  admin_enabled       = true  # TODO: Use Managed Identity in production

  tags = {
    Name = "${var.app_name}-acr"
  }
}

# ==============================================================================
# Log Analytics Workspace - Required for Container Apps
# ==============================================================================

resource "azurerm_log_analytics_workspace" "logs" {
  name                = "${var.app_name}-logs"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "PerGB2018"
  retention_in_days   = 30  # TODO: Increase for production

  tags = {
    Name = "${var.app_name}-logs"
  }
}

# ==============================================================================
# Container App Environment - Shared environment for Container Apps
# ==============================================================================

resource "azurerm_container_app_environment" "env" {
  name                       = "${var.app_name}-env"
  resource_group_name        = azurerm_resource_group.main.name
  location                   = azurerm_resource_group.main.location
  log_analytics_workspace_id = azurerm_log_analytics_workspace.logs.id

  tags = {
    Name = "${var.app_name}-env"
  }
}

# ==============================================================================
# Container App - The actual deployment
# ==============================================================================

resource "azurerm_container_app" "app" {
  name                         = var.app_name
  resource_group_name          = azurerm_resource_group.main.name
  container_app_environment_id = azurerm_container_app_environment.env.id
  revision_mode                = "Single"  # TODO: Use "Multiple" for blue-green

  template {
    container {
      name   = var.app_name
      image  = "${azurerm_container_registry.acr.login_server}/${var.app_name}:${var.image_tag}"
      cpu    = var.cpu
      memory = var.memory

      env {
        name  = "ENVIRONMENT"
        value = var.environment
      }

      env {
        name  = "PORT"
        value = var.app_port
      }

      # TODO: Add secrets from Azure Key Vault
      # env {
      #   name        = "OPENAI_API_KEY"
      #   secret_name = "openai-api-key"
      # }

      # Dynamic environment variables
      dynamic "env" {
        for_each = var.environment_variables
        content {
          name  = env.key
          value = env.value
        }
      }
    }

    min_replicas = var.min_replicas
    max_replicas = var.max_replicas
  }

  # Ingress configuration for web traffic
  ingress {
    external_enabled = true
    target_port      = var.app_port
    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }

  # Registry credentials
  registry {
    server               = azurerm_container_registry.acr.login_server
    username             = azurerm_container_registry.acr.admin_username
    password_secret_name = "acr-password"
  }

  secret {
    name  = "acr-password"
    value = azurerm_container_registry.acr.admin_password
  }

  # TODO: Add secrets for your app
  # secret {
  #   name  = "openai-api-key"
  #   value = var.openai_api_key
  # }

  tags = {
    Name = var.app_name
  }
}

# ==============================================================================
# Outputs - Important URLs and info
# ==============================================================================

output "app_url" {
  description = "URL of the deployed application"
  value       = "https://${azurerm_container_app.app.ingress[0].fqdn}"
}

output "acr_login_server" {
  description = "ACR login server URL for pushing images"
  value       = azurerm_container_registry.acr.login_server
}

output "acr_admin_username" {
  description = "ACR admin username"
  value       = azurerm_container_registry.acr.admin_username
  sensitive   = true
}

output "acr_admin_password" {
  description = "ACR admin password"
  value       = azurerm_container_registry.acr.admin_password
  sensitive   = true
}

output "resource_group_name" {
  description = "Resource group name"
  value       = azurerm_resource_group.main.name
}

output "container_app_name" {
  description = "Container App name"
  value       = azurerm_container_app.app.name
}
