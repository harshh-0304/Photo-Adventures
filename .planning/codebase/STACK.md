# Technology Stack

**Analysis Date:** 2026-03-22

## Languages

**Primary:**
- Python 3.x - Django backend framework

**Secondary:**
- HTML5 - Template rendering
- CSS3/JavaScript - Frontend (Bootstrap 5, jQuery)

## Runtime

**Environment:**
- Python 3 with Django 3.2.18

**Package Manager:**
- pip (requirements.txt)
- No lockfile present

## Frameworks

**Core:**
- Django 3.2.18 - Web framework
- django-allauth 0.x - Authentication and account management

**Frontend:**
- Bootstrap 5.2.3 - CSS framework
- jQuery 3.6.3 - JavaScript library
- AOS (Animate on Scroll) 2.3.1 - Scroll animations

**Admin/Editor:**
- django-summernote - Rich text editor for post content
- django-crispy-forms + crispy-bootstrap5 - Form rendering

**Storage:**
- django-taggit - Tag management
- Pillow - Image processing
- django-social-share - Social media sharing buttons

## Key Dependencies

**Authentication:**
- django-allauth - User registration, login, OAuth
- PyJWT - JWT token handling (listed but not actively used in current config)

**Database:**
- dj-database-url - Database URL parsing
- psycopg2 - PostgreSQL adapter (production)
- sqlite3 - Django default (development)

**Image Storage:**
- cloudinary - Cloud image storage (configured but commented out)
- dj3-cloudinary-storage - Cloudinary Django integration (installed but disabled)

**Deployment:**
- gunicorn - WSGI application server
- dj-database-url - Heroku PostgreSQL integration

## Configuration

**Environment:**
- Uses `env.py` for environment variables (not committed)
- Falls back to `os.environ.get()` for secrets
- Settings: `photoadventures/settings.py`

**Build:**
- No build tools (Django native)
- Static files served from `static/` directory
- Static files collected to `staticfiles/` for deployment

## Platform Requirements

**Development:**
- Python 3.x
- SQLite (default)
- No external services required

**Production:**
- PostgreSQL database
- Cloudinary for image storage
- SMTP server for email (Gmail configured)

---

*Stack analysis: 2026-03-22*
