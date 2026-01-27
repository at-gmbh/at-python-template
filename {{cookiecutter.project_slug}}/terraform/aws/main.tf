# ==============================================================================
# AWS App Runner Deployment - Simple & Transparent
# ==============================================================================
#
# 🎯 PHILOSOPHY: "Infrastructure as Code that you can understand"
#
# This Terraform config deploys your Docker container to AWS App Runner.
# App Runner is the SIMPLEST way to run containers on AWS (like Heroku).
#
# 🚀 CUSTOMIZATION: Everything here is a starting point. Adjust as needed!
# - Switch to ECS Fargate for more control
# - Add RDS database
# - Add CloudFront CDN
# - Add custom domain
#
# ==============================================================================

terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # TODO: Configure remote state (S3 + DynamoDB)
  # backend "s3" {
  #   bucket = "my-terraform-state"
  #   key    = "{{ cookiecutter.project_slug }}/terraform.tfstate"
  #   region = "us-east-1"
  # }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "{{ cookiecutter.project_name }}"
      ManagedBy   = "Terraform"
      Environment = var.environment
    }
  }
}

# ==============================================================================
# ECR Repository - Where your Docker images live
# ==============================================================================

resource "aws_ecr_repository" "app" {
  name                 = var.app_name
  image_tag_mutability = "MUTABLE"  # TODO: Use "IMMUTABLE" for production

  # Keep last N images, delete old ones
  image_scanning_configuration {
    scan_on_push = true  # Security scanning
  }

  tags = {
    Name = "${var.app_name}-ecr"
  }
}

# Lifecycle policy - Keep only last 10 images
resource "aws_ecr_lifecycle_policy" "app" {
  repository = aws_ecr_repository.app.name

  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "Keep last 10 images"
      selection = {
        tagStatus     = "any"
        countType     = "imageCountMoreThan"
        countNumber   = 10
      }
      action = {
        type = "expire"
      }
    }]
  })
}

# ==============================================================================
# IAM Role for App Runner
# ==============================================================================

# IAM role that App Runner uses to pull from ECR
resource "aws_iam_role" "apprunner_ecr_access" {
  name = "${var.app_name}-apprunner-ecr-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "build.apprunner.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

# Attach ECR read policy
resource "aws_iam_role_policy_attachment" "apprunner_ecr_access" {
  role       = aws_iam_role.apprunner_ecr_access.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess"
}

# IAM role for the app itself (for accessing AWS services)
resource "aws_iam_role" "apprunner_instance" {
  name = "${var.app_name}-apprunner-instance-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "tasks.apprunner.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

# TODO: Add policies if your app needs AWS services
# resource "aws_iam_role_policy_attachment" "s3_access" {
#   role       = aws_iam_role.apprunner_instance.name
#   policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
# }

# ==============================================================================
# App Runner Service - The actual deployment
# ==============================================================================

resource "aws_apprunner_service" "app" {
  service_name = var.app_name

  source_configuration {
    authentication_configuration {
      access_role_arn = aws_iam_role.apprunner_ecr_access.arn
    }

    image_repository {
      image_identifier      = "${aws_ecr_repository.app.repository_url}:${var.image_tag}"
      image_repository_type = "ECR"

      image_configuration {
        # TODO: Adjust port based on your UI framework
        port = var.app_port  # 8000 for Chainlit, 8501 for Streamlit

        # Environment variables
        runtime_environment_variables = merge(
          var.environment_variables,
          {
            ENVIRONMENT = var.environment
            PORT        = tostring(var.app_port)
          }
        )

        # Secrets from AWS Secrets Manager
        # TODO: Store OPENAI_API_KEY in Secrets Manager
        # runtime_environment_secrets = {
        #   OPENAI_API_KEY = "arn:aws:secretsmanager:region:account:secret:openai-key"
        # }
      }
    }

    auto_deployments_enabled = var.auto_deploy
  }

  instance_configuration {
    instance_role_arn = aws_iam_role.apprunner_instance.arn
    cpu               = var.cpu
    memory            = var.memory
  }

  health_check_configuration {
    protocol            = "HTTP"
    path                = "/"
    interval            = 10
    timeout             = 5
    healthy_threshold   = 1
    unhealthy_threshold = 5
  }

  tags = {
    Name = var.app_name
  }
}

# ==============================================================================
# Outputs - Important URLs and info
# ==============================================================================

output "app_url" {
  description = "URL of the deployed application"
  value       = "https://${aws_apprunner_service.app.service_url}"
}

output "ecr_repository_url" {
  description = "ECR repository URL for pushing images"
  value       = aws_ecr_repository.app.repository_url
}

output "service_arn" {
  description = "App Runner service ARN"
  value       = aws_apprunner_service.app.arn
}

output "service_id" {
  description = "App Runner service ID"
  value       = aws_apprunner_service.app.service_id
}
