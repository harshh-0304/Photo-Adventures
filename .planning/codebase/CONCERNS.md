# Codebase Concerns

**Analysis Date:** 2026-03-22

## Tech Debt

**Hardcoded Secret Key:**
- Issue: Django SECRET_KEY is hardcoded in settings.py
- Files: `photoadventures/settings.py` line 26
- Impact: Security vulnerability if committed to version control
- Fix: Move to `env.py` or environment variable

**Debug Mode:**
- Issue: `DEBUG = True` is hardcoded
- Files: `photoadventures/settings.py` line 29
- Impact: Security risk in production
- Fix: `DEBUG = os.environ.get('DEBUG', 'False') == 'True'`

**Cloudinary Configured but Disabled:**
- Issue: Cloudinary packages installed but storage disabled
- Files: `photoadventures/settings.py` lines 47-49, 176-177, 181-182
- Impact: Confusion, unused dependencies, potential migration issues
- Fix: Either enable Cloudinary or remove unused packages

**Database Configuration:**
- Issue: SQLite for development, PostgreSQL commented out
- Files: `photoadventures/settings.py` lines 126-136
- Impact: Development/production mismatch
- Fix: Use environment-based switching properly

**Settings Environment Variables:**
- Issue: `env.py` exists but critical vars like `DATABASE_URL` read directly
- Files: `photoadventures/settings.py` line 13-14
- Impact: Inconsistent environment handling
- Fix: Standardize on environment variables

## Known Bugs

**Duplicate Blog URLs:**
- Issue: Blog page accessible at both `/` and `/blog/`
- Files: `photoadventures/urls.py` lines 23, 35
- Root cause: Root URL (`''`) points to `views.index` which may show blog content
- Fix: Redirect `/` to `/blog/` or differentiate content

**Duplicate Add Post URLs:**
- Issue: `/add_post/` defined twice
- Files: `photoadventures/urls.py` line 42, `blog/urls.py` line 15
- Impact: Potential routing confusion
- Fix: Remove duplicate from main urls.py

**Template Typo:**
- Issue: `ACCOUNG_SIGNUP_PASSWORD_VERIFICATION` (typo)
- Files: `photoadventures/settings.py` line 205
- Impact: This setting won't work
- Fix: Change to `ACCOUNT_SIGNUP_PASSWORD_VERIFICATION`

**Comment Method Typo:**
- Issue: `rerunt` instead of `return` in docstring
- Files: `blog/models.py` line 44
- Impact: Documentation only, no runtime impact
- Fix: Correct typo

**Duplicate User Check:**
- Issue: `{% if user.is_authenticated %}` checked twice in base.html
- Files: `templates/base.html` lines 46-47
- Impact: Minor redundancy
- Fix: Remove duplicate condition

**Gravatar Default URL:**
- Issue: Hardcoded Cloudinary URL as default
- Files: `blog/templatetags/gravatar.py` line 25
- Impact: External dependency on Cloudinary even when disabled
- Fix: Use local default or no-cache URL

## Security Considerations

**CSRF Enabled:** Yes (Django default middleware)

**XSS Protection:** Django template auto-escaping enabled

**SQL Injection:** Protected via Django ORM

**Email Passwords in Code:**
- Risk: `EMAIL_HOST_PASSWORD` stored in env.py
- Current mitigation: env.py not committed
- Recommendations: Use environment variables, not file

**Admin Access:**
- Risk: Direct `/admin/` access enabled
- Current mitigation: Requires authentication
- Recommendations: Consider restricting in production

## Performance Bottlenecks

**N+1 Query Problem:**
- Problem: Multiple queries in `index()` view for statistics
- Files: `blog/views.py` lines 43-51
- Cause: Separate queries for posts, comments, likes, users
- Improvement: Use a single aggregation or cache

**Unfiltered Querysets:**
- Problem: `Post.objects.count()` runs full table scan
- Files: `blog/views.py` lines 47-51
- Cause: No indexing on `status` field
- Improvement: Add database indexes

**No Pagination on Home:**
- Problem: Index view may load all posts if no likes
- Files: `blog/views.py` lines 43-44
- Impact: Could be slow with many posts
- Improvement: Add pagination

## Fragile Areas

**URL Configuration:**
- Files: `photoadventures/urls.py`, `blog/urls.py`
- Why fragile: Duplicate patterns, scattered includes
- Safe modification: Use namespaced includes

**Cloudinary Integration:**
- Files: Multiple in settings.py, templates reference Cloudinary
- Why fragile: Half-implemented, may break if re-enabled
- Safe modification: Full refactor or complete removal

**Status Workflow:**
- Files: `blog/models.py`, `blog/constants.py`, `blog/views.py`
- Why fragile: Magic numbers (0, 1, 2) used throughout
- Safe modification: Use constants consistently

## Scaling Limits

**Database:** SQLite (dev) / PostgreSQL (prod)
- Current capacity: Sufficient for small blog
- Limit: PostgreSQL recommended for production
- Scaling path: Add read replicas for high traffic

**Static Files:** Local storage
- Current capacity: Limited
- Limit: File system storage won't scale
- Scaling path: Enable Cloudinary or use CDN

**Image Storage:** Local filesystem
- Current capacity: Server-dependent
- Limit: Storage fills up, no CDN
- Scaling path: Enable Cloudinary

## Dependencies at Risk

**Django 3.2.18:**
- Risk: LTS version but approaching end of support
- Impact: Security patches will stop
- Migration plan: Upgrade to Django 4.2 LTS or 5.x

**PyJWT:**
- Risk: Listed in requirements but not used
- Impact: Unused dependency
- Migration plan: Remove from requirements.txt

**django-allauth (older version):**
- Risk: May have security vulnerabilities
- Impact: Authentication compromise
- Migration plan: Upgrade to latest version

## Missing Critical Features

**No Tests:**
- Problem: Zero test coverage
- Blocks: Safe refactoring, CI/CD confidence
- Priority: HIGH

**No API:**
- Problem: No REST API for mobile/app clients
- Blocks: Mobile app development, third-party integrations
- Priority: MEDIUM

**No Caching:**
- Problem: Every request hits database
- Blocks: Performance under load
- Priority: MEDIUM

**No Rate Limiting:**
- Problem: No protection against spam/abuse
- Blocks: Comment spam, brute force
- Priority: MEDIUM

## Test Coverage Gaps

**Models:**
- What's not tested: Post creation, Comment approval workflow
- Files: `blog/models.py`
- Risk: Model methods may break silently
- Priority: HIGH

**Views:**
- What's not tested: All views (CRUD, authentication flows)
- Files: `blog/views.py`
- Risk: Breaking changes go unnoticed
- Priority: HIGH

**Forms:**
- What's not tested: Validation, required fields
- Files: `blog/forms.py`
- Risk: Invalid data may be accepted
- Priority: MEDIUM

**URL Routing:**
- What's not tested: All URL patterns
- Risk: Broken routes
- Priority: MEDIUM

---

*Concerns audit: 2026-03-22*
