# Codebase Structure

**Analysis Date:** 2026-03-22

## Directory Layout

```
Photo-Adventures/
├── blog/                  # Main Django app
├── photoadventures/        # Django project settings
├── templates/             # HTML templates
├── static/                 # CSS, JS, images
├── docs/                  # Documentation
├── .planning/             # GSD planning docs
├── manage.py              # Django CLI
├── requirements.txt       # Dependencies
├── Procfile               # Heroku deployment
├── README.md              # Project documentation
└── 1.py                   # Unknown (appears stray)
```

## Directory Purposes

**`blog/`:**
- Purpose: Main application containing all blog functionality
- Contains: models.py, views.py, urls.py, forms.py, admin.py, tests.py, constants.py, templatetags/
- Key files: `models.py` (Post, Comment), `views.py` (all views)

**`photoadventures/`:**
- Purpose: Django project configuration
- Contains: settings.py, urls.py, wsgi.py, asgi.py
- Key files: `settings.py` (all configuration)

**`templates/`:**
- Purpose: HTML templates for all pages
- Contains: base.html, blog.html, full_post.html, account/ (AllAuth), socialaccount/ (OAuth), openid/
- Key files: `base.html` (main layout)

**`static/`:**
- Purpose: Static assets
- Contains: css/style.css, js/*.js, favicon/
- Key files: `css/style.css`, `js/script.js`

**`docs/`:**
- Purpose: Additional documentation
- Status: Needs exploration

**`.planning/`:**
- Purpose: GSD methodology planning documents
- Generated: Yes
- Committed: Yes

## Key File Locations

**Entry Points:**
- `manage.py`: Django management CLI
- `photoadventures/wsgi.py`: WSGI application (gunicorn target)

**Configuration:**
- `photoadventures/settings.py`: All Django settings
- `photoadventures/urls.py`: Root URL configuration
- `requirements.txt`: Python dependencies
- `Procfile`: Heroku deployment config

**Core Logic:**
- `blog/models.py`: Post, Comment models
- `blog/views.py`: All view logic (CBVs and FBVs)
- `blog/forms.py`: CommentForm, PostForm
- `blog/constants.py`: Status choices, categories, template names

**Testing:**
- `blog/tests.py`: Empty (tests not implemented)

## Naming Conventions

**Files:**
- Lowercase with underscores: `blog_views.py` (not used)
- Current pattern: `models.py`, `views.py`, `forms.py`
- Constants: `constants.py` with UPPER_SNAKE_CASE values

**Directories:**
- Lowercase with underscores: `blog/`, `templates/`, `static/`

**URL Names:**
- Snake case: `post_like`, `user_account`, `full_post`, `tagged_posts`

## Where to Add New Code

**New Feature:**
- Primary code: `blog/views.py`
- Model additions: `blog/models.py`
- URL routing: `blog/urls.py`
- Template: `templates/`
- Tests: `blog/tests.py` (currently empty)

**New Model:**
- Model definition: `blog/models.py`
- Admin registration: `blog/admin.py`
- Form (if needed): `blog/forms.py`
- View: `blog/views.py`
- URL: `blog/urls.py`

**New Template:**
- Base templates: `templates/base.html`
- App templates: `templates/` root
- AllAuth templates: `templates/account/`

**Utilities:**
- Template tags: `blog/templatetags/gravatar.py`
- Constants: `blog/constants.py`

## Special Directories

**`blog/migrations/`:**
- Purpose: Database migration files
- Generated: Yes
- Committed: Yes
- Count: 21 migration files (many for field alterations)

**`templates/account/`:**
- Purpose: AllAuth authentication templates
- Source: django-allauth default templates (customized)
- Contains: login, signup, password reset, email confirmation

**`templates/socialaccount/`:**
- Purpose: OAuth provider templates
- Source: django-allauth social account templates
- Customized: signup.html, login.html, connections.html

**`static/favicon/`:**
- Purpose: Favicon images
- Generated: Yes (from Cloudinary)

---

*Structure analysis: 2026-03-22*
