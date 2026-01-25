# HTTPS Deployment Notes (Apache/Nginx)

## Overview
This project enforces HTTPS at the Django level using:
- SECURE_SSL_REDIRECT = True
- HSTS headers (SECURE_HSTS_SECONDS, INCLUDE_SUBDOMAINS, PRELOAD)
- Secure cookies (SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE)

## SSL/TLS Certificates
Use a trusted certificate authority (e.g., Let's Encrypt) to obtain certificates:
- fullchain.pem
- privkey.pem

## Example Nginx Configuration (Conceptual)
- Terminate TLS at Nginx using the certificate files.
- Forward requests to Django (Gunicorn/Uvicorn) over localhost.
- Set X-Forwarded-Proto so Django recognizes HTTPS.

Key directives:
- listen 443 ssl;
- ssl_certificate /path/fullchain.pem;
- ssl_certificate_key /path/privkey.pem;
- proxy_set_header X-Forwarded-Proto https;

## Example Apache Notes (Conceptual)
- Enable SSL module and configure VirtualHost :443.
- Point SSLCertificateFile and SSLCertificateKeyFile to your cert paths.
- Ensure proxy headers indicate HTTPS.
