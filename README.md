# Cloud Resume Challenge

Multi-cloud serverless resume website built for the [Cloud Resume Challenge](https://cloudresumechallenge.dev/) via the [ExamPro bootcamp](https://www.exampro.co/crc-cpb-000).

## Live Sites

- **AWS**: [www.danphillipsonline.com](https://www.danphillipsonline.com)
- **GCP**: [danphillips.cloud](https://danphillips.cloud)

## Architecture

Same resume site deployed on two cloud platforms:

- **AWS**: CloudFormation, S3, CloudFront, Lambda, DynamoDB, Route 53
- **GCP**: Terraform, GCS, Cloud Functions, Firestore, Cloudflare

Both use Ansible for deployment automation and share the same frontend/backend code.

## Documentation

- [Frontend](./frontend/README.md) - Static HTML/CSS/JS resume with visitor counter
- [Backend](./backend/README.md) - Python build scripts and mock API for local development
- [AWS](./aws/README.md) - CloudFormation infrastructure and deployment
- [GCP](./gcp/README.md) - Terraform infrastructure and deployment

