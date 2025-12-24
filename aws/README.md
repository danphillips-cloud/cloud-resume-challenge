# AWS Playbooks

## Using Cloudformation

For AWS I'll be using CloudFormation. I could use Terraform but for this challenge I wanted to explore the infra, so since CF is native to AWS it makes sense. I'll use Terraform for GCP

My plan is to not use a VPC, which can get expensive, and use this architecture.

Route 53 (danphillipsonline.com)  
    ↓  
CloudFront (with ACM certificate for HTTPS)  
    ↓  
S3 Bucket (static website files)

CloudFront also connects to:  
    ↓  
API Gateway (/api/counter)  
    ↓  
Lambda (visitor counter logic, NO VPC)  
    ↓  
DynamoDB (stores the count)

## Install Ansible

```sh
pipx install --include-deps ansible
ansible-galaxy collection install amazon.aws

```
