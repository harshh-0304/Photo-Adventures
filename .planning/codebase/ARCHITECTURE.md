# Architecture

**Analysis Date:** 2026-03-22

## Pattern Overview

**Overall:** Traditional Django MVC/MVT with Django AllAuth for authentication

**Key Characteristics:**
- Single app (`blog`) with core functionality
- Function-based and class-based views mixed
- Template inheritance for UI consistency
- Status-based content moderation (Draft → Moderation → Published)

## Layers

**URL/Routing:**
- Purpose: Route URLs to views
- Location: `photoadventures/urls.py` (main), `blog/urls.py` (app)
- Contains: URL patterns for all endpoints
- Depends on: Views module
- Used by: Django URL dispatcher

**Views (Controllers):**
- Purpose: Handle HTTP request/response logic
- Location: `blog/views.py`
- Contains: CBVs (BlogPosts, FullPost, PostLike, PostEdit, TaggedPosts) and FBVs (index, about, contact, add_post, delete_post, user_account)
- Depends on: Models, Forms
- Used by: URL routing

**Models (Data):**
- Purpose: Database schema and business logic
- Location: `blog/models.py`
- Contains: Post, TaggedPost, Comment models
- Depends on: Django ORM, taggit
- Used by: Views, Admin, Forms

**Forms (Input):**
- Purpose: Handle form validation and rendering
- Location: `blog/forms.py`
- Contains: CommentForm, PostForm
- Depends on: Models
- Used by: Views, Templates

**Templates (Presentation):**
- Purpose: HTML rendering with Django template language
- Location: `templates/`
- Contains: base.html, blog.html, full_post.html, etc.
- Depends on: Views (context)
- Used by: Views (via render())

**Admin:**
- Purpose: Content management interface
- Location: `blog/admin.py`
- Contains: PostAdmin (SummernoteModelAdmin), CommentAdmin
- Depends on: Models
- Used by: Site administrators

## Data Flow

**Viewing a Blog Post:**
1. User navigates to `/blog/<slug>/`
2. `FullPost.as_view()` receives GET request
3. Query: `Post.objects.filter(status=2, slug=slug)`
4. Fetch approved comments: `post.comments.filter(approved=True)`
5. Check if user liked: `post.likes.filter(id=user.id).exists()`
6. Render `full_post.html` with context

**Creating a Comment:**
1. User submits comment form (POST to same URL)
2. `FullPost.post()` processes request
3. Validate `CommentForm` with `request.POST`
4. Set `email` and `name` from authenticated user
5. Save comment with `approved=False`
6. Display success message awaiting approval
7. Re-render template with updated state

**User Creates Post:**
1. Authenticated user submits `PostForm` (POST to `/add_post/`)
2. Validate form including image upload
3. Set `author=request.user`
4. Save with `commit=False`, then `save()` and `save_m2m()` for tags
5. Redirect to user dashboard

## Key Abstractions

**Post Model:**
- Purpose: Blog post content with author, category, tags, likes
- Examples: `blog/models.py` line 9-53
- Pattern: Django Model with ForeignKey, ManyToMany, TaggableManager

**Status Workflow:**
- Purpose: Content moderation workflow
- Pattern: Integer choices (0=Draft, 1=Moderation, 2=Published)
- Usage: All queries filter by `status=2` for published content

**Custom Template Tags:**
- Purpose: Generate Gravatar URLs from email
- Location: `blog/templatetags/gravatar.py`
- Usage: `{{ user.email|gravatar }}` in templates

## Entry Points

**Main Application:**
- Location: `photoadventures/wsgi.py`
- Triggers: `gunicorn photoadventures.wsgi` or `python manage.py runserver`
- Responsibilities: WSGI application factory

**URL Configuration:**
- Location: `photoadventures/urls.py`
- Triggers: HTTP requests
- Responsibilities: Route to views, include AllAuth/Summernote URLs

**Blog URLs:**
- Location: `blog/urls.py`
- Triggers: URLs prefixed with `/blog/`
- Responsibilities: Blog post CRUD, likes, tags

## Error Handling

**Strategy:** Django default + custom messages framework

**Patterns:**
- `get_object_or_404()` for 404 errors
- `messages.success/warning()` for user feedback
- Custom 404/500 error templates in `templates/`

## Cross-Cutting Concerns

**Logging:** Default Django logging (console only)

**Validation:** Django forms + model field validators

**Authentication:** Django AllAuth with email verification

**CSRF Protection:** Enabled by default in middleware

**XSS Protection:** Template auto-escaping (Django default)

---

*Architecture analysis: 2026-03-22*
