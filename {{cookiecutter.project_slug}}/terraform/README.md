# 🚀 Terraform Infrastructure - Unified Cloud Deployment

**Philosophy:** Single Source of Truth - Same syntax for AWS and Azure!

---

## 📁 Structure

```
terraform/
├── aws/                # AWS App Runner deployment
│   ├── main.tf
│   └── variables.tf
└── azure/              # Azure Container Apps deployment
    ├── main.tf
    └── variables.tf
```

---

## 🎯 Why Terraform for Both Clouds?

**Benefits:**
- ✅ **Single Syntax** - Learn once, use everywhere
- ✅ **Version Control** - Infrastructure as Code in Git
- ✅ **State Management** - Track changes, rollback easily
- ✅ **Consistency** - Same deployment process for all clouds
- ✅ **Modularity** - Reusable components
- ✅ **Plan Before Apply** - See changes before they happen

**vs. Cloud-Specific Tools:**
- AWS CloudFormation: AWS-only, YAML/JSON
- Azure CLI: Imperative, no state management
- **Terraform: Universal, declarative, stateful** ✨

---

## 🚀 Quick Start

### AWS Deployment

```bash
# 1. Navigate to AWS Terraform
cd terraform/aws

# 2. Initialize Terraform
terraform init

# 3. Review the plan
terraform plan

# 4. Apply (creates infrastructure)
terraform apply

# 5. Get the app URL
terraform output app_url
```

### Azure Deployment

```bash
# 1. Navigate to Azure Terraform
cd terraform/azure

# 2. Login to Azure
az login

# 3. Initialize Terraform
terraform init

# 4. Review the plan
terraform plan

# 5. Apply (creates infrastructure)
terraform apply

# 6. Get the app URL
terraform output app_url
```

---

## ⚙️ Configuration

### Customize via Variables

**Method 1: terraform.tfvars file**
```terraform
# terraform/aws/terraform.tfvars
app_name    = "my-custom-name"
aws_region  = "eu-central-1"
cpu         = "2048"
memory      = "4096"
```

**Method 2: Command-line flags**
```bash
terraform apply \
  -var="app_name=my-app" \
  -var="cpu=2048"
```

**Method 3: Environment variables**
```bash
export TF_VAR_app_name="my-app"
export TF_VAR_cpu="2048"
terraform apply
```

### Key Variables

#### AWS (`terraform/aws/variables.tf`)
- `aws_region` - AWS region (default: us-east-1)
- `app_name` - Application name
- `image_tag` - Docker image tag
- `cpu` - CPU units (1024 = 1 vCPU)
- `memory` - Memory in MB (2048 = 2GB)

#### Azure (`terraform/azure/variables.tf`)
- `location` - Azure region (default: westeurope)
- `resource_group_name` - Resource group name
- `app_name` - Application name
- `image_tag` - Docker image tag
- `cpu` - CPU cores (0.5, 1.0, 2.0)
- `memory` - Memory (1.0Gi, 2.0Gi)

---

## 🔐 Secrets Management

### DO NOT commit secrets to Git!

**AWS: Use AWS Secrets Manager**
```terraform
# Uncomment in main.tf
resource "aws_secretsmanager_secret" "openai_key" {
  name = "openai-api-key"
}

resource "aws_secretsmanager_secret_version" "openai_key" {
  secret_id     = aws_secretsmanager_secret.openai_key.id
  secret_string = var.openai_api_key  # Pass via TF_VAR
}
```

**Azure: Use Azure Key Vault**
```terraform
# Uncomment in main.tf
resource "azurerm_key_vault" "kv" {
  name                = "${var.app_name}-kv"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"
}

resource "azurerm_key_vault_secret" "openai_key" {
  name         = "openai-api-key"
  value        = var.openai_api_key
  key_vault_id = azurerm_key_vault.kv.id
}
```

---

## 📊 State Management (Production)

### Remote State with S3 (AWS)

```terraform
# terraform/aws/main.tf
terraform {
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "{{ cookiecutter.project_slug }}/terraform.tfstate"
    region = "us-east-1"

    # Enable state locking
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

**Setup:**
```bash
# Create S3 bucket
aws s3 mb s3://my-terraform-state

# Create DynamoDB table for locking
aws dynamodb create-table \
  --table-name terraform-locks \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST
```

### Remote State with Azure Storage (Azure)

```terraform
# terraform/azure/main.tf
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "tfstate"
    container_name       = "tfstate"
    key                  = "{{ cookiecutter.project_slug }}.tfstate"
  }
}
```

**Setup:**
```bash
# Create resource group
az group create --name terraform-state-rg --location westeurope

# Create storage account
az storage account create \
  --name tfstate \
  --resource-group terraform-state-rg \
  --location westeurope \
  --sku Standard_LRS

# Create blob container
az storage container create \
  --name tfstate \
  --account-name tfstate
```

---

## 🔄 CI/CD Integration

### GitHub Actions (Automated)

**Enable workflows:**
```bash
# For AWS
mv .github/workflows/deploy_aws.yml.disabled \
   .github/workflows/deploy_aws.yml

# For Azure
mv .github/workflows/deploy_azure.yml.disabled \
   .github/workflows/deploy_azure.yml
```

**Set GitHub Secrets:**
- AWS: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
- Azure: `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`

---

## 🧹 Cleanup / Destroy

```bash
# AWS
cd terraform/aws
terraform destroy

# Azure
cd terraform/azure
terraform destroy
```

**Warning:** This deletes ALL resources! Use with caution.

---

## 📚 Terraform Commands Cheat Sheet

```bash
# Initialize (download providers)
terraform init

# Format code
terraform fmt

# Validate configuration
terraform validate

# See what will change
terraform plan

# Apply changes
terraform apply

# Show current state
terraform show

# List outputs
terraform output

# Destroy infrastructure
terraform destroy

# Import existing resource
terraform import <resource_type>.<name> <id>

# Refresh state
terraform refresh
```

---

## 🎯 Best Practices

### 1. Always Run Plan First
```bash
terraform plan -out=tfplan
terraform apply tfplan
```

### 2. Use Variables
```bash
# Don't hardcode values
resource "aws_instance" "app" {
  instance_type = "t3.micro"  # ❌ Bad
}

# Use variables
resource "aws_instance" "app" {
  instance_type = var.instance_type  # ✅ Good
}
```

### 3. Use Remote State (Production)
- Local state = Single point of failure
- Remote state = Team collaboration, locking, backup

### 4. Tag Everything
```terraform
tags = {
  Project     = "{{ cookiecutter.project_name }}"
  Environment = var.environment
  ManagedBy   = "Terraform"
}
```

### 5. Use Modules for Reusability
```terraform
module "app" {
  source = "./modules/container-app"

  app_name = var.app_name
  cpu      = var.cpu
  memory   = var.memory
}
```

---

## 🐛 Troubleshooting

### Issue: "Error: No valid credential sources"
**Solution (AWS):** Run `aws configure` or set `AWS_ACCESS_KEY_ID`

**Solution (Azure):** Run `az login`

### Issue: "Backend initialization required"
**Solution:** Run `terraform init`

### Issue: "State lock timeout"
**Solution:** Someone else is applying. Wait or force-unlock:
```bash
terraform force-unlock <lock-id>
```

### Issue: "Resource already exists"
**Solution:** Import existing resource:
```bash
terraform import <resource>.<name> <id>
```

---

## 📖 Resources

- [Terraform Documentation](https://www.terraform.io/docs)
- [AWS Provider Docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Azure Provider Docs](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)

---

## ✅ Summary

**You now have:**
- ✅ Unified Terraform for AWS + Azure
- ✅ Infrastructure as Code (version controlled)
- ✅ Automated CI/CD workflows
- ✅ State management
- ✅ Secrets management patterns

**Next steps:**
1. Choose your cloud (`aws` or `azure`)
2. Customize `variables.tf`
3. Run `terraform apply`
4. Deploy! 🚀
