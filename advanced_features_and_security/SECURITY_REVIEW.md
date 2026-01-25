# Security Review Report

## Measures Implemented
1. HTTPS enforcement
- SECURE_SSL_REDIRECT forces HTTPS connections.
- HSTS settings instruct browsers to only use HTTPS for 1 year and include subdomains, with preload enabled.

2. Secure cookies
- SESSION_COOKIE_SECURE and CSRF_COOKIE_SECURE ensure cookies are sent only over HTTPS.

3. Security headers
- X_FRAME_OPTIONS="DENY" prevents clickjacking via iframes.
- SECURE_CONTENT_TYPE_NOSNIFF reduces MIME-sniffing risks.
- SECURE_BROWSER_XSS_FILTER enables browser XSS filtering.

## Why this helps
These settings reduce exposure to MITM attacks, cookie theft, clickjacking, and certain XSS/MIME confusion attacks.

## Potential improvements
- Use a reverse proxy with proper SECURE_PROXY_SSL_HEADER.
- Add CSP (Content Security Policy) and tighten directives based on used assets.
- Enable logging/monitoring and rotate secrets using environment variables.
