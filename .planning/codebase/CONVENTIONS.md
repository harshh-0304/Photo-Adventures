# Coding Conventions

**Analysis Date:** 2026-03-22

## Naming Patterns

**Files:**
- Lowercase with underscores: `models.py`, `views.py`, `forms.py`
- Constants file: `constants.py` with UPPER_SNAKE_CASE values

**Functions:**
- snake_case for function names: `add_post()`, `delete_post()`, `dashboard_stats()`
- Verb-noun pattern for actions

**Variables:**
- snake_case: `user_name`, `user_email`, `trending`
- Descriptive but concise
- Query variables prefixed or suffixed: `draft_count`, `awaiting_moderation_count`

**Types/Classes:**
- PascalCase: `BlogPosts`, `FullPost`, `PostLike`, `PostEdit`, `TaggedPosts`
- Model classes: `Post`, `Comment`, `TaggedPost`
- Form classes: `CommentForm`, `PostForm`
- Admin classes: `PostAdmin`, `CommentAdmin`

## Code Style

**Formatting:**
- No explicit formatter configured (no black, autopep8)
- Manual formatting observed
- Indentation: 4 spaces

**Linting:**
- No ESLint (Python project)
- No flake8/pylint configured
- Django default code style

## Import Organization

**Order in `views.py`:**
1. Django built-ins: `from django.shortcuts import ...`
2. Django views: `from django.views import ...`
3. Django HTTP: `from django.http import ...`
4. Internal modules: `from blog import constants as CONST`
5. Django ORM: `from django.db.models import ...`
6. Local imports: `from .models import Post, Comment`
7. Form imports: `from .forms import CommentForm, PostForm`
8. Auth: `from django.contrib.auth.models import User`
9. Auth decorators: `from django.contrib.auth.decorators import login_required`
10. Auth mixins: `from django.contrib.auth.mixins import LoginRequiredMixin`
11. Messages: `from django.contrib import messages`
12. Template: `from django.template.loader import render_to_string`
13. Taggit: `from taggit.models import Tag`

**Pattern:** Groups by Django module, then local imports

**No Path Aliases:**
- No `from blog.constants import CONST` (uses `as` instead)

## Error Handling

**Patterns:**
- `get_object_or_404(queryset, slug=slug)` - Raise 404 if not found
- `form.is_valid()` with inline error display
- `try/except` not commonly used (relies on Django 404)

**Message Usage:**
- `messages.success(request, 'text')` - Positive feedback
- `messages.warning(request, 'text')` - Destructive actions
- Messages displayed via Bootstrap toast in base.html

## Logging

**Framework:** Python print / Django messages framework

**Patterns:**
- User-facing messages via `django.contrib.messages`
- No structured logging
- No log levels configured

## Comments

**When to Comment:**
- All public methods have docstrings
- Docstrings explain purpose, parameters, return values
- Some typos in docstrings (e.g., "rerunt" instead of "return")

**JSDoc/TSDoc:**
- Not applicable (Python project)
- Python docstrings used instead

## Function Design

**Size:** 
- Functions typically < 50 lines
- Views handle single responsibilities
- Helper functions extracted (e.g., `dashboard_stats()`)

**Parameters:**
- Standard Django patterns: `request`, optional `slug`, `*args`, `**kwargs`
- CBV methods: `self`, `request`, optional args

**Return Values:**
- Views return `render(request, template, context)` or `HttpResponseRedirect`
- Helper functions return context dictionaries or querysets

## Module Design

**Exports:**
- Django models exported via `from .models import Post, Comment`
- Forms via `from .forms import CommentForm, PostForm`
- Constants via `from blog import constants as CONST`

**Barrel Files:**
- None (Django pattern uses explicit imports)

---

*Convention analysis: 2026-03-22*
