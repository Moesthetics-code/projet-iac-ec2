variable "region" {
  description = "Région AWS"
  type        = string
  default     = "eu-north-1"
}

variable "instance_os" {
  description = "AMI ID pour l'instance"
  type        = string
  
  validation {
    condition     = can(regex("^ami-[a-z0-9]{8,}$", var.instance_os))
    error_message = "L'AMI doit commencer par 'ami-'."
  }
}

variable "instance_name" {
  description = "Nom de l'instance"
  type        = string
  
  validation {
    condition     = length(var.instance_name) > 0 && length(var.instance_name) <= 50
    error_message = "Le nom doit contenir entre 1 et 50 caractères."
  }
}

variable "instance_size" {
  description = "Type d'instance EC2"
  type        = string
  default     = "t3.micro"
  
  validation {
    condition     = contains(["t3.micro", "t3.small", "t3.medium", "t2.micro"], var.instance_size)
    error_message = "Type invalide."
  }
}

variable "instance_env" {
  description = "Environnement"
  type        = string
  
  validation {
    condition     = contains(["dev", "preprod", "prod"], var.instance_env)
    error_message = "L'environnement doit être dev, preprod ou prod."
  }
}
