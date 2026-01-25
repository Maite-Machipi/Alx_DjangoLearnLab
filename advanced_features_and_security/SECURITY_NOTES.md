# Security Measures Implemented

## Settings (settings.py)
- DEBUG=False (production safe default)
- SECURE_BROWSER_XSS_FILTER=True
- SECURE_CONTENT_TYPE_NOSNIFF=True
- X_FRAME_OPTIONS="DENY"
- CSRF_COOKIE_SECURE=True
- SESSION_COOKIE_SECURE=True

## CSRF Protection
- All POST forms include `{% csrf_token %}` (see form_example.html).

## SQL Injection Prevention
- Views use Django ORM filtering instead of raw SQL.
- User input is validated using Django Forms (`BookSearchForm`) and accessed via `cleaned_data`.

## CSP (Content Security Policy)
- Implemented with django-csp middleware and CSP_* settings to reduce XSS risk.
