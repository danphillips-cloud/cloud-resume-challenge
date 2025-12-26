## Install Terraform - WIP

I will be using Terraform for IaC with GCP as that is the recommended method and widely used in the industry. 

I already have Terraform installed but you can install this using the docs from https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli

### Terraform and GCP Authentication

I created a new service account in GCP and gave it Infrastructure Administration permissions to create the resources I will need for the project. 

![](/gcp/images/tf-access.png)

I will need to set this enviornment variable so that Terraform can autheticate to GCP. I would sugget setting this as an enviornment variable locally or in A CodeSpace.
```sh
export GOOGLE_APPLICATION_CREDENTIALS=/danph/cloud-resume-challenge/gcp/gcp-key.json
```

I have soooooooooooooo much more to add. My GCP + Terrform journey was wroght with IAM issues, but I got it done. danphillips.cloud is now live on GCP. 