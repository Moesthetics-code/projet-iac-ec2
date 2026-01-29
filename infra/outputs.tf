output "instance_id" {
  description = "ID de l'instance EC2"
  value       = aws_instance.ec2_demo.id
}

output "instance_public_ip" {
  description = "Adresse IP publique"
  value       = aws_instance.ec2_demo.public_ip
}

output "instance_private_ip" {
  description = "Adresse IP privée"
  value       = aws_instance.ec2_demo.private_ip
}

output "instance_state" {
  description = "État de l'instance"
  value       = aws_instance.ec2_demo.instance_state
}

output "instance_public_dns" {
  description = "DNS public"
  value       = aws_instance.ec2_demo.public_dns
}

output "security_group_id" {
  description = "ID du security group"
  value       = aws_security_group.ec2_sg.id
}

output "instance_az" {
  description = "Zone de disponibilité"
  value       = aws_instance.ec2_demo.availability_zone
}

output "ssh_command" {
  description = "Commande SSH pour se connecter"
  value       = "ssh -i votre-cle.pem ec2-user@${aws_instance.ec2_demo.public_ip}"
}