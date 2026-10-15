# 📷 Photo Adventures

[![Django CI](https://github.com/harshh-0304/Photo-Adventures/actions/workflows/django_ci.yml/badge.svg)](https://github.com/harshh-0304/Photo-Adventures/actions/workflows/django_ci.yml)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0+-green.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Photo Adventures** is an interactive photography community and blogging platform built with Django. Photographers, travelers, and storytellers can publish adventures, discover content by category or location, discuss photography techniques, and share stunning visuals.

---

## 🚀 Key Features

- **User Accounts & Authentication**: Secure registration, login, profile management, and password reset workflows powered by `django-allauth`.
- **Adventure Publishing (CRUD)**: Create, preview, edit, and manage photo stories with draft saving and moderation status workflows.
- **Dynamic Reading Estimation**: Automatic reading time calculation on posts based on word count.
- **Real-Time Popularity & View Counting**: Post views are tracked atomically and displayed alongside like counters and comment counts.
- **Search & Filtering**:
  - Full-text keyword search across titles, captions, content, and locations.
  - Category-based browsing (Landscape, Wildlife, Travel, Architecture, Aerial, Street, Nature, Adventure).
  - Hashtag taxonomy powered by `django-taggit`.
  - Author profile archives.
- **Interactive Discussion**: Moderated comment system with Gravatar avatar integration and bulk admin moderation tools.
- **Adjacent Adventure Navigation**: Seamless previous/next story navigation on every article.
- **JSON API**: Public REST endpoint for trending adventures (`/blog/api/posts/trending/`).
- **SEO & Observability**:
  - Built-in `robots.txt` and XML sitemap generator endpoints.
  - Production `/health/` monitoring endpoint for uptime probes.
  - Open Graph social metadata for rich link previews.

---

## 🛠️ Tech Stack

- **Backend Framework**: Django 6.x / Python 3.11 & 3.12
- **Database**: PostgreSQL (production) / SQLite (development)
- **Frontend & Styling**: HTML5, Vanilla CSS, Bootstrap 5, FontAwesome 6, AOS (Animate on Scroll)
- **Media & Assets**: Cloudinary (`dj3-cloudinary-storage`), Gravatar
- **CI / CD**: GitHub Actions (`django_ci.yml`)
- **WSGI / Deployment**: Gunicorn, WhiteNoise / Cloudinary

---

## 📁 Repository Structure

```text
Photo-Adventures/
├── .github/
│   └── workflows/
│       └── django_ci.yml       # Automated GitHub Actions test workflow
├── blog/
│   ├── migrations/             # Database schema migrations
│   ├── templatetags/           # Custom template filters (blog_extras, gravatar)
│   ├── tests/                  # Automated test suite (models, views, forms, comments)
│   ├── admin.py                # Post and Comment administration & bulk actions
│   ├── constants.py            # Categories, status codes, and pagination config
│   ├── forms.py                # PostForm and CommentForm with validation rules
│   ├── models.py               # Post, Comment, and custom PostQuerySet
│   ├── urls.py                 # URL patterns for blog routes and API endpoints
│   └── views.py                # Class-based and function-based views
├── photoadventures/
│   ├── settings.py             # Project settings with secure environment fallbacks
│   ├── urls.py                 # Root URL configuration and health endpoints
│   └── wsgi.py                 # WSGI entry point for web servers
├── static/                     # CSS, JavaScript, and custom styling
├── templates/                  # Base and application HTML templates
├── manage.py                   # Django CLI management script
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

---

## 📦 Getting Started

### 1. Prerequisites

- Python 3.11+
- Git
- Virtual environment (`venv`)

### 2. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/harshh-0304/Photo-Adventures.git
cd Photo-Adventures

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file or export the following variables:

```bash
SECRET_KEY=your-secure-random-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3  # or postgres://user:password@localhost:5432/dbname
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
```

### 4. Database Setup & Migrations

```bash
python manage.py migrate
python manage.py createsuperuser  # Optional, for admin dashboard access
```

### 5. Run the Local Development Server

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 🧪 Running Automated Tests

Run the full automated test suite:

```bash
python manage.py test
```

To run individual test modules:

```bash
python manage.py test blog.tests.test_models    # Post model & custom queryset tests
python manage.py test blog.tests.test_comments  # Comment relation & truncation tests
python manage.py test blog.tests.test_views     # Page & API integration tests
python manage.py test blog.tests.test_forms     # PostForm and CommentForm tests
```

---

## 🌐 API & Utility Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/health/` | `GET` | System health check returning database status |
| `/robots.txt` | `GET` | Search engine crawler instructions and sitemap link |
| `/sitemap.xml` | `GET` | XML sitemap of all published adventure stories |
| `/blog/api/posts/trending/` | `GET` | JSON API returning top trending posts |
| `/blog/search/?q=<query>` | `GET` | Keyword search across titles, content & locations |
| `/blog/category/<name>/` | `GET` | Filter stories by category |
| `/blog/author/<username>/` | `GET` | Author story archives |

---

## 🤝 Contributing

Contributions are welcome!
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
