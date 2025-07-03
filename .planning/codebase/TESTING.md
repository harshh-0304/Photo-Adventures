# Testing Patterns

**Analysis Date:** 2026-03-22

## Test Framework

**Runner:**
- Django's built-in test runner
- Command: `python manage.py test`
- Config: Django default (no pytest, no coverage configured)

**Assertion Library:**
- Django's `unittest.TestCase`
- Django-specific assertions: `assertEqual`, `assertContains`, etc.

**Run Commands:**
```bash
python manage.py test              # Run all tests
python manage.py test blog         # Run blog app tests
python manage.py test --verbosity=2  # Verbose output
```

## Test File Organization

**Location:**
- Primary: `blog/tests.py`
- **Status:** EMPTY - No tests implemented

**Pattern:** Co-located with app (Django convention)

**Naming:** `tests.py` (standard Django)

## Test Structure

**Suite Organization:**
```python
# Currently empty - only boilerplate
from django.test import TestCase

# Create your tests here.
```

**No actual tests exist.**

## Mocking

**Framework:** Django's unittest.mock (standard library)

**Patterns:** Unknown (no tests to analyze)

**What to Mock:**
- External services (email, Cloudinary)
- Authentication (for view tests)
- Database queries (for performance tests)

**What NOT to Mock:**
- ORM operations in integration tests

## Fixtures and Factories

**Test Data:**
- No fixtures defined
- No factory pattern in use
- Would need factories for User, Post, Comment

**Location:**
- `blog/fixtures/` - Does not exist
- Would typically go in `blog/fixtures/`

## Coverage

**Requirements:** None enforced

**View Coverage:** Not configured

## Test Types

**Unit Tests:**
- Not implemented

**Integration Tests:**
- Not implemented

**E2E Tests:**
- Not implemented (no Selenium, Playwright, or Cypress)

## Common Patterns

**Async Testing:** Not applicable

**Error Testing:** Not implemented

## Critical Gap

**No tests exist in the project.**

---

*Testing analysis: 2026-03-22*
