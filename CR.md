# Change Record - CORS Configuration Enhancement & Custom Domain

## API Gateway CORS Configuration
- Enhanced CORS settings in CloudFormation template (aws/backend-counter.yaml)
- Added explicit `AllowCredentials: false` setting to API Gateway configuration
- Expanded allowed headers to include `X-Requested-With` for AJAX request compatibility
- Configured preflight cache duration with MaxAge: 600 seconds
- Restricted origin to `https://www.danphillipsonline.com` for security

## Lambda Function CORS Headers
- Updated Lambda response headers to align with API Gateway CORS configuration
- Added comprehensive CORS headers to both successful and error responses
- Included `Access-Control-Max-Age` header for preflight request caching
- Ensured consistent header handling across all response paths

## Custom Domain Configuration
- Added custom domain support for API Gateway using `api.danphillipsonline.com`
- Created API Gateway custom domain name resource with TLS 1.2 security policy
- Configured base path mapping to route requests to prod stage
- Added Route53 A record with alias to API Gateway custom domain
- Updated frontend visitor-counter.js to use custom domain URL
- Added CloudFormation parameters for domain name, ACM certificate, and hosted zone ID

## Deployment Notes & Known Issues

### CloudFormation Deployment Gotchas
1. **Route53 Record Creation Delays**: The ApiDNSRecord resource can take 60+ seconds to create, causing the stack update to appear hung. This is normal AWS behavior - Route53 alias records take time to propagate.

2. **Pre-existing Custom Domains**: If `api.danphillipsonline.com` was manually created before deploying this stack, CloudFormation will fail with "AlreadyExists" error. Solution: Delete the existing custom domain and Route53 records before deployment:
   ```bash
   aws apigateway delete-domain-name --domain-name api.danphillipsonline.com --region us-east-1
   ```

3. **Manual Resource Deletion**: Never manually delete CloudFormation-managed resources (like Route53 records) while a stack update is in progress. This causes drift and unpredictable behavior.

4. **Template Caching**: SAM may cache templates. Always run `sam build -t backend-counter.yaml` after template changes, and use `--force-upload` flag if deployment shows "no changes" incorrectly.

### Deployment Command
```bash
sam build -t backend-counter.yaml
sam deploy --force-upload --parameter-overrides \
  DomainName=api.danphillipsonline.com \
  ACMCertificateArn=arn:aws:acm:us-east-1:ACCOUNT_ID:certificate/CERT_ID \
  HostedZoneId=HOSTED_ZONE_ID
```

## Benefits
- Ensures proper cross-origin request handling from danphillipsonline.com
- Reduces preflight request frequency through cache configuration
- Maintains security by restricting allowed origins
- Provides consistent CORS behavior across API Gateway and Lambda layers
- Professional custom domain (api.danphillipsonline.com) instead of AWS-generated URL
- Cleaner API endpoint for frontend integration
