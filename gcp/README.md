# GCP Infrastructure

Terraform-based serverless infrastructure with Ansible deployment automation and Cloudflare CDN.

## Overview

The GCP infrastructure uses Terraform for resource management and Ansible for deployment automation. The architecture is serverless with public GCS bucket hosting, Cloud Functions for the visitor counter, and Cloudflare providing CDN and SSL termination.

## Features

- **Terraform Infrastructure**: Industry-standard IaC with remote state in Terraform Cloud
- **Ansible Deployment**: Automated terraform workflow and content uploads
- **Serverless Architecture**: Cloud Functions v2, Firestore—no compute instances
- **GCS Static Hosting**: Public bucket with direct access and Cloudflare caching
- **Cloudflare CDN**: Free SSL, global CDN, and DDoS protection
- **Service Account Security**: Dedicated service account for Cloud Function runtime

## Architecture

```
Cloudflare (danphillips.cloud)
    ↓ (Proxy + SSL)
GCS Bucket (public read)
    ↓
Static website files

Cloudflare also proxies to:
    ↓
Cloud Functions v2 (/api/counter)
    ↓
Firestore (visitor count storage)
```

**Key Design Choices:**
- **Public GCS Bucket**: Simpler than private bucket + Cloud CDN, Cloudflare handles security
- **Cloudflare vs Cloud CDN**: Free tier includes SSL, faster global edge network
- **Firestore vs Datastore**: Native mode Firestore for better Firebase integration
- **Terraform Cloud State**: Remote state with version history

## Quick Start

### Prerequisites

Install Terraform, gcloud CLI, and Ansible:

```bash
# Terraform
# Follow: https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli

# gcloud CLI
# Follow: https://cloud.google.com/sdk/docs/install

# Ansible (if not already installed)
pipx install --include-deps ansible
```

### Configure GCP Authentication

Create a service account with appropriate permissions:

1. Go to GCP Console → IAM & Admin → Service Accounts
2. Create service account: `terraform-deploy`
3. Grant roles (see Permissions section below)
4. Create and download JSON key file

**Security Note:** The service account key will be stored encrypted in Ansible Vault. Never commit unencrypted credentials to version control.

### Configure Ansible Vault

Store credentials in an encrypted vault (similar to AWS approach):

```bash
cd gcp/ansible
ansible-vault create group_vars/all/vault.yml
```

Add the following, replacing the `gcp_service_account_json` value with the **entire contents** of your downloaded JSON key file:

```yaml
gcp_service_account_json: |
  {
    "type": "service_account",
    "project_id": "your-project-id",
    "private_key_id": "abc123...",
    "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_KEY_HERE\n-----END PRIVATE KEY-----\n",
    "client_email": "terraform-deploy@your-project.iam.gserviceaccount.com",
    "client_id": "123456789",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
  }

cloudflare_api_token: your-cloudflare-api-token
cloudflare_zone_id: your-cloudflare-zone-id
```

See `group_vars/all/vault.yml.example` for a template.

Store vault password in `../../.vault_pass` (gitignored).

**UPDATE:** I changed how GCP credentials work to match the AWS approach. The old way stored a file path in the vault (`gcp_service_account_key: /path/to/key.json`), which meant you had to download the key file on every machine and manually export `GOOGLE_APPLICATION_CREDENTIALS`. Pain in the ass when switching between my Mac and work laptop.

Now the playbooks store the entire service account JSON directly in the vault. When you run a playbook, it creates a temporary credential file from the vault contents, uses it for authentication with `gcloud auth activate-service-account`, then cleans it up automatically in post_tasks. Switch machines? Just need the vault password. No key files to manage, no environment variables to remember.

Copy the **entire JSON file contents** into `gcp_service_account_json`, not just the path. Same clean workflow as AWS.

## Directory Structure

```text
gcp/
├── README.md                  # This file
├── terraform/
│   ├── main.tf                # Main infrastructure definition
│   ├── variables.tf           # Input variables
│   ├── outputs.tf             # Output values
│   └── function/              # Cloud Function source code
│       ├── main.py            # Visitor counter logic
│       └── requirements.txt   # Python dependencies
├── ansible/
│   ├── deploy-gcp.yml         # Deploy Terraform infrastructure
│   ├── upload-gcp.yml         # Upload files + purge Cloudflare cache
│   ├── destroy-gcp.yml        # Tear down infrastructure
└── images/                    # Architecture diagrams and documentation screenshots

```

## Deployment

### Deploy Infrastructure

Deploy the Terraform infrastructure via Ansible:

```bash
cd gcp/ansible
ansible-playbook deploy-gcp.yml --vault-password-file ../../.vault_pass
```

This will:
1. Validate Terraform configuration
2. Initialize Terraform with remote state
3. Plan infrastructure changes
4. Prompt for confirmation
5. Apply changes and create:
   - GCS bucket for static hosting
   - Cloud Function v2 for visitor counter
   - Firestore database (if not exists)
   - Service account for function runtime
   - Required API enablements

**Important:** After deployment, you must manually grant Firestore permissions to the function service account (see Permissions section).

### Upload Website Files

After infrastructure is ready and permissions are configured:

```bash
ansible-playbook upload-gcp.yml --vault-password-file ../../.vault_pass
```

This will:
1. Sync files from `frontend/public/` to GCS bucket
2. Set cache control headers (HTML: 5min, CSS/JS: 1yr)
3. Purge Cloudflare cache
4. Display access URLs

### Destroy Infrastructure

To tear down all GCP resources:

```bash
ansible-playbook destroy-gcp.yml --vault-password-file ../../.vault_pass
```

## Configuration

### Domain Setup

- **Primary URL**: `https://danphillips.cloud` (via Cloudflare)
- **WWW URL**: `https://www.danphillips.cloud` (via Cloudflare)
- **Direct GCS**: `https://storage.googleapis.com/danphillips.cloud/index.html`

### Required GCP Permissions

**For Terraform Service Account:**
- `Storage Admin` - Manage GCS buckets
- `Cloud Functions Developer` - Deploy functions
- `Service Account User` - Impersonate service accounts
- `Service Usage Admin` - Enable APIs
- `Project IAM Admin` - Manage IAM bindings (if allowed by org policy)

**For Cloud Function Runtime Service Account:**
- `Cloud Datastore User` - Read/write Firestore (must be granted manually)

**Manual Permission Grant (Required):**

After deploying, grant Firestore access to the function:

```bash
gcloud projects add-iam-policy-binding danphillips-cloud-crc \
  --member="serviceAccount:visitor-counter-sa@danphillips-cloud-crc.iam.gserviceaccount.com" \
  --role="roles/datastore.user"
```

Or via GCP Console: IAM & Admin → Grant the service account `Cloud Datastore User` role.

---

## Development Journey

This section documents the design decisions and challenges while building the GCP infrastructure. I'm sure I'll make adjustments as I learn more, but this is how it all started.

### Choosing Terraform

I used Terraform for GCP instead of native tools. It's the industry standard for multi-cloud IaC, and I wanted hands-on experience with it.

### The IAM Permission Challenge

**GCP IAM is complex.** Organization policies, project-level restrictions, service-specific permissions—it makes AWS IAM look simple.

I hit so many permission errors during deployment. A few examples:

- Need `Service Usage Admin` just to enable APIs via Terraform
- Need `Service Account User` to create resources that use service accounts
- Organization policies blocked IAM bindings, forcing manual Firestore permission grants

After the third error, I understood why people just grant `Owner` or `Editor` and move on. It works, but it's bad security. I wanted just start with least-privilege, but it took patience.

![](./images/tf-access.png)

**AWS vs GCP**: With AWS, I set up IAM once and it worked. With GCP, every step hit a permission wall. AWS CloudFormation? Smooth. GCP Terraform? Error-driven development.

![](./images/hello-world-api.png)

![](./images/firestore-working.png)

### Cloudflare for CDN and SSL

I used Cloudflare's free tier instead of Google Cloud CDN and Load Balancer. Free SSL, better global edge network, DDoS protection, and easier cache purging. The public GCS bucket works perfectly behind Cloudflare's proxy.

### Terraform Cloud for State

I store Terraform state in Terraform Cloud instead of GCS. Version history, state locking, and it's free for personal projects.

### Other Decisions

**Cloud Functions v2**: Better performance than v1, built on Cloud Run. Required enabling yet another API.

**Firestore**: Native mode instead of Datastore. More intuitive transactions and works with Firebase.

### Lessons Learned

- Document every permission. Save future you (and others) hours of debugging.
- Start with minimal permissions, add as errors occur. Takes longer but you learn what's actually needed.
- Some org policies force manual steps. Accept it, document it, move on.
- Cloudflare free tier beats Cloud CDN for personal projects.
- GCP Terraform errors are verbose but helpful—read them carefully.
- **Credential Management**: Storing JSON credentials directly in Ansible Vault (like the AWS setup) is cleaner than managing key files. No need to export `GOOGLE_APPLICATION_CREDENTIALS` or sync files across machines. The playbooks handle temporary credential files automatically.

---

## Troubleshooting

**Terraform fails with "API not enabled":**

Enable required APIs manually:
```bash
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable firestore.googleapis.com
```

**Cloud Function deployment fails with permission error:**

Check the Terraform service account has these roles:
- Cloud Functions Developer
- Service Account User
- Storage Admin

**Function returns 500 error when called:**

The function service account likely doesn't have Firestore access. Grant it manually:
```bash
gcloud projects add-iam-policy-binding danphillips-cloud-crc \
  --member="serviceAccount:visitor-counter-sa@danphillips-cloud-crc.iam.gserviceaccount.com" \
  --role="roles/datastore.user"
```

**Terraform state locked:**

If Terraform crashes mid-deployment, the state may be locked in Terraform Cloud. Unlock it:
- Go to Terraform Cloud → Workspace → Settings → Force unlock

**Cloudflare cache not purging:**

Verify `cloudflare_api_token` and `cloudflare_zone_id` in vault are correct. Check token has "Purge Cache" permission.

---

## Cost Considerations

**GCP Free Tier (monthly):**
- Cloud Functions: 2M invocations, 400K GB-seconds
- Cloud Storage: 5GB, 5K Class A operations, 50K Class B operations
- Firestore: 1GB storage, 50K reads, 20K writes, 20K deletes

**Cloudflare Free Tier:**
- Unlimited bandwidth
- Global CDN
- Free SSL certificates
- DDoS protection

This setup should cost $0/month for personal resume traffic.


## Diagram

![](./images/gcp-infra.drawio.png)

This was my first attempt at diagraming GCP. I know it isn't complete but frankly I have no interest in using GCP for hosting this site. It's too complex for what I need and is IAM Hell. 
