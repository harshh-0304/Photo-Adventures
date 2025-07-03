# External Integrations

**Analysis Date:** 2026-03-22

## APIs & External Services

**Image Storage:**
- Cloudinary - Image hosting (SDK: `cloudinary`, `dj3-cloudinary-storage`)
  - Auth: `CLOUDINARY_URL` environment variable
  - Status: Installed but **DISABLED** (default storage uses `FileSystemStorage`)

**Social Authentication:**
- Django AllAuth OAuth providers
  - Auth: Configured via AllAuth social accounts
  - Status: Templates present but no active providers configured

**Social Sharing:**
- django-social-share - Share buttons
  - Endpoints: Twitter, Facebook sharing
  - Templates: `templates/django_social_share/templatetags/`

**Gravatar:**
- External Gravatar service for user avatars
  - URL pattern: `https://www.gravatar.com/avatar/{hash}`
  - Default placeholder: Cloudinary-hosted image

## Data Storage

**Database:**
- **Development:** SQLite (`db.sqlite3`)
  - Connection: `BASE_DIR / 'db.sqlite3'`
- **Production:** PostgreSQL
  - Connection: `DATABASE_URL` via `dj_database_url`
  - Client: `psycopg2`

**File Storage:**
- **Local:** `django.core.files.storage.FileSystemStorage` (default)
  - Media directory: `MEDIA_ROOT` (default)
  - Upload path: `featured_images/`
- **Cloud:** Cloudinary (configured but disabled)

**Caching:**
- None detected

## Authentication & Identity

**Auth Provider:**
- Django AllAuth (email-based authentication)
  - Email verification: Mandatory
  - Login method: Email (not username)
  - Login attempts: 3 per 60 seconds
  - Email confirmation expires: 1 day
  - Password reset: Email-based (Django auth views)

**Session Management:**
- Django sessions middleware
- Cookie-based sessions

## Monitoring & Observability

**Error Tracking:**
- None detected

**Logs:**
- Django logging (default console)
- Heroku logging via gunicorn

## CI/CD & Deployment

**Hosting:**
- Heroku (primary target)
  - Procfile: `web: gunicorn photoadventures.wsgi`
  - Configured in `Procfile`

**CI Pipeline:**
- None detected (no GitHub Actions, no test automation)

## Environment Configuration

**Required env vars:**
```
SECRET_KEY=your-secret-key
DEBUG=True/False
DATABASE_URL=postgres://...
CLOUDINARY_URL=cloudinary://...
EMAIL_HOST_USER=gmail-address
EMAIL_HOST_PASSWORD=gmail-app-password
DEFAULT_FROM_EMAIL=from-email
```

**Secrets location:**
- `env.py` (imported conditionally)
- Heroku config vars (production)

## Webhooks & Callbacks

**Incoming:**
- None detected

**Outgoing:**
- None configured

---

*Integration audit: 2026-03-22*
