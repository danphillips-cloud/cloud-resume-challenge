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

## Benefits
- Ensures proper cross-origin request handling from danphillipsonline.com
- Reduces preflight request frequency through cache configuration
- Maintains security by restricting allowed origins
- Provides consistent CORS behavior across API Gateway and Lambda layers
- Professional custom domain (api.danphillipsonline.com) instead of AWS-generated URL
- Cleaner API endpoint for frontend integration
