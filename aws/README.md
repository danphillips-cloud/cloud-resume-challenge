# AWS Playbooks

## Architecture Overview

For this challenge, I'm using **CloudFormation** for AWS infrastructure. While I could use Terraform for everything, I wanted to explore AWS-native tooling since CF integrates directly with AWS services. I'll switch to Terraform for the GCP implementation to compare both approaches.

The architecture is serverless and VPC-free to keep costs within free tier limits:
```
Route 53 (danphillipsonline.com)
    ↓
CloudFront (ACM certificate for HTTPS)
    ↓
S3 Bucket (static website files)

CloudFront also connects to:
    ↓
API Gateway (/api/counter)
    ↓
Lambda (visitor counter logic, NO VPC)
    ↓
DynamoDB (visitor count storage)
```

**Key Design Choices:**
- **No VPC**: Lambda runs in AWS-managed environment (free tier eligible)
- **CloudFront + OAC**: Private S3 buckets with secure CloudFront access
- **Serverless**: Pay only for what you use (essentially free for this traffic)

## Prerequisites

### Install Ansible and Dependencies

I'm using Ansible for deployment automation.
```sh
pipx install --include-deps ansible
pipx inject ansible boto3 botocore
ansible-galaxy collection install amazon.aws
```

### Configure AWS Credentials

Create an encrypted vault to store AWS credentials securely:
```sh
# Create encrypted vault file
ansible-vault create vaults/prod.yml

# You'll be prompted for a vault password, then add:
# AWS_REGION: us-east-1
# AWS_ACCESS_KEY_ID: your-key-id
# AWS_SECRET_ACCESS_KEY: your-secret-key
# STACK_NAME: your-cloudformation-stack-name
```

**Security Note:** The vault password itself is stored in `.vault_pass` (gitignored). Never commit credentials to version control.

## Deployment Workflow

### Deploy Infrastructure (CloudFormation Stack)

This creates/updates all AWS resources defined in `template.yaml`:
```sh
cd aws/playbooks
ansible-playbook deploy.yml --vault-password-file ../../.vault_pass
```

**What gets deployed:**
- S3 buckets (www + apex redirect)
- CloudFront distributions (2 total)
- Origin Access Control (OAC)
- Bucket policies
- Stack outputs (distribution IDs, URLs)

### Upload Website Files

After infrastructure is ready, deploy your static site:
```sh
ansible-playbook upload.yml --vault-password-file ../../.vault_pass
```

**What happens:**
1. Validates `frontend/public/` directory exists
2. Syncs files to `www.danphillipsonline.com` S3 bucket
3. Deletes files from S3 that don't exist locally (clean deploys)
4. Invalidates CloudFront cache (`/*` all files)
5. New content live in ~30-60 seconds

## Current Infrastructure

### Domain Setup

- **Primary URL**: `https://www.danphillipsonline.com` (main site)
- **Apex Redirect**: `https://danphillipsonline.com` → redirects to www
- **SSL Certificate**: Wildcard ACM cert (`*.danphillipsonline.com`)

### CloudFront Distributions

Two distributions handle different purposes:

1. **WWW Distribution** (ID: `E3J4QYS4EHJHOH`)
   - Serves content from `www.danphillipsonline.com` bucket
   - Private bucket with OAC (Origin Access Control)
   - Cache invalidation on every deploy

2. **Apex Distribution** (ID: `EEN5OIGV5JHHT`)
   - Handles redirect from apex → www
   - Sources from `danphillipsonline.com` bucket (S3 website redirect)

### Why WWW as Primary?

I initially set up apex (`danphillipsonline.com`) as primary with www redirecting to it. After consideration, I reversed this for several reasons:

1. **Clear bucket identification**: `www.danphillipsonline.com` bucket = website files, `danphillipsonline.com` bucket = redirect only
2. **Future subdomain flexibility**: Keeps apex free for `api.danphillipsonline.com`, `blog.danphillipsonline.com`, etc.
3. **Industry pattern**: Many large sites use www as canonical (stackoverflow.com, github.com uses apex, but both are valid)
4. **Operational clarity**: When debugging, it's immediately clear which bucket holds actual content

The redirect bucket never needs files uploaded to it - it's purely for S3 website redirect configuration.

### S3 Bucket Strategy

- **www.danphillipsonline.com**: Private bucket, holds all static files (HTML, CSS, JS, assets)
- **danphillipsonline.com**: Public redirect bucket, configured with S3 website hosting to 301 redirect all requests to www

Both buckets are free tier eligible. The redirect bucket uses almost no storage or bandwidth.

## Project Structure
```
cloud-resume-challenge/
├── aws/
│   ├── playbooks/
│   │   ├── deploy.yml      # CloudFormation stack deployment
│   │   └── upload.yml      # S3 sync + cache invalidation
│   └── template.yaml       # CloudFormation infrastructure
├── frontend/
│   └── public/             # Static website files
│       ├── index.html
│       ├── assets/
│       │   ├── styles.css
│       │   └── script.js
│       └── ...
├── vaults/
│   └── prod.yml            # Encrypted credentials (gitignored)
├── .vault_pass             # Vault password (gitignored)
└── .gitignore
```

## Development Notes

### Lessons Learned

1. **Git Security**: Had to remove vault files from git history after initial commits. Always check `.gitignore` before first commit.

2. **CloudFormation Parameters**: Changing parameter names (e.g., `BucketName` → `DomainName`) requires stack recreation, not just update.

3. **OAC vs OAI**: Origin Access Control (OAC) is the modern replacement for Origin Access Identity (OAI). Better security, recommended by AWS.

4. **Cache Invalidation**: Critical to invalidate CloudFront cache after uploads, otherwise users see stale content for hours.

5. **Distribution ID Tracking**: With multiple CloudFront distributions, it's important to track which ID corresponds to which purpose (www vs apex).

### Troubleshooting

**Stack stuck in UPDATE_ROLLBACK_COMPLETE?**
```sh
# Check status
aws cloudformation describe-stacks --stack-name your-stack-name --region us-east-1

# Delete and redeploy if needed
aws cloudformation delete-stack --stack-name your-stack-name --region us-east-1
```

**Vault password lost?**
Recreate the vault file with new credentials:
```sh
ansible-vault create vaults/prod.yml
echo "your-new-password" > .vault_pass
chmod 600 .vault_pass
```

## Next Steps: Visitor Counter

The next phase implements a serverless visitor counter:

1. **DynamoDB Table**: Stores visit count with atomic increment
2. **Lambda Function**: Python function to increment and return count
3. **API Gateway**: REST endpoint at `api.danphillipsonline.com/counter`
4. **Frontend Integration**: JavaScript fetch() to display count
5. **Infrastructure as Code**: Terraform for API resources