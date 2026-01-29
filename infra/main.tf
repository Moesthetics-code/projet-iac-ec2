terraform {
  required_version = ">= 1.0"
  
  required_providers {
  aws = {
    source  = "hashicorp/aws"
    version = "~> 6.0"
  }
}
}

provider "aws" {
  region = var.region
}

# Récupérer le VPC par défaut
data "aws_vpc" "default" {
  default = true
}

# Récupérer les subnets du VPC par défaut
data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# Créer un security group
resource "aws_security_group" "ec2_sg" {
  name        = "${var.instance_name}-sg"
  description = "Security group for ${var.instance_name}"
  vpc_id      = data.aws_vpc.default.id

  # SSH
  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTP
  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTPS
  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Tout le trafic sortant
  egress {
    description = "Allow all outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.instance_name}-sg"
    Environment = var.instance_env
    ManagedBy   = "Terraform"
    Project     = "Sonatel-IAC"
  }
}

# Créer l'instance EC2
resource "aws_instance" "ec2_demo" {
  ami                    = var.instance_os
  instance_type          = var.instance_size
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]
  subnet_id              = data.aws_subnets.default.ids[0]
  
  # Activer l'IP publique
  associate_public_ip_address = true

  tags = {
    Name        = var.instance_name
    Environment = var.instance_env
    ManagedBy   = "Terraform"
    Project     = "Sonatel-IAC"
  }

  lifecycle {
    create_before_destroy = true
  }
}