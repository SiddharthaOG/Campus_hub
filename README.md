# Campus Resource Hub

A modern Django-based platform for students to share and discover academic resources (notes, previous year papers, lab manuals, study materials) with social features like upvotes, comments, and user following.

![Django](https://img.shields.io/badge/Django-4.2-green)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Tests](https://img.shields.io/badge/Tests-36_passing-brightgreen)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-336791)

## Features

### Core Functionality
- **Resource Library**: Browse, search, and filter academic resources by subject, semester, branch, and type
- **File Previews**: Inline PDF viewer and image previews for uploaded files
- **External Links**: Support for Google Drive, GitHub, and other external resource links
- **Download Tracking**: Automatic download counting

### Social Features
- **Upvotes**: Reddit-style upvoting on resources with real-time updates (HTMX)
- **Comments**: Threaded comments with auto-filled username for logged-in users
- **User Profiles**: Public profiles showing uploaded resources, bio, branch, year, hosteller status
- **Follow System**: Follow/unfollow users, mutual followers detection
- **Career Upvotes**: Aggregate upvote count across all user's resources

### Admin & Management
- **Supercharged Admin**: Featured resources toggle, branch/semester/type filters, date hierarchy, bulk actions
- **Resource Ownership**: Track who uploaded each resource
- **File Storage**: Local development, Supabase/PostgreSQL ready, Cloudinary/AWS S3 configurable

### Modern Stack
- **Django 4.2** with class-based patterns
- **HTMX** for dynamic interactions without heavy JS frameworks
- **Bootstrap 5** with custom CSS variables for theming
- **PostgreSQL** (Supabase) with SQLite fallback for local dev
- **36 automated tests** covering models, views, auth, and social features

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL (or use SQLite for local dev)
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/SiddharthaOG/Campus-Hub.git
cd Campus-Hub

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your settings (see Configuration below)

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# (Optional) Seed with sample data
python seed_data.py
python seed_files.py

# Collect static files
python manage.py collectstatic --noinput

# Run development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to see the app.

## Configuration

Create a `.env` file in the project root:

```env
# Database (Supabase/Postgres URL). Leave empty to use local SQLite.
DATABASE_URL=postgresql://user:password@host:port/dbname

# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here-generate-with-python-secrets-module
ALLOWED_HOSTS=localhost,127.0.0.1

# File Storage (optional)
# Cloudinary
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# AWS S3 (alternative)
USE_S3=False
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_STORAGE_BUCKET_NAME=your_bucket
AWS_S3_REGION_NAME=us-east-1
```

### Production Settings
Set these in your production environment:
```env
DEBUG=False
SECRET_KEY=<generate with: python -c "import secrets; print(secrets.token_urlsafe(50))">
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://...
```

Security settings (HSTS, SSL redirect, secure cookies) activate automatically when `DEBUG=False`.

## Project Structure

```
Campus-Hub/
├── campus_hub/           # Project settings
│   ├── settings.py       # Main configuration
│   ├── urls.py           # Root URL routing
│   └── wsgi.py
├── resources/            # Main app
│   ├── models.py         # Resource, Comment models
│   ├── views.py          # Resource CRUD, search, upvotes, comments
│   ├── forms.py          # ResourceForm, CommentForm, SignUpForm
│   ├── urls.py           # Resource URLs
│   ├── admin.py          # Supercharged admin config
│   ├── templatetags/     # Custom template filters
│   ├── partials/         # HTMX partial templates
│   ├── tests.py          # 19 tests
│   └── migrations/
├── users/                # User profiles & social
│   ├── models.py         # Profile, Follow models
│   ├── views.py          # Profile, follow, edit views
│   ├── forms.py          # ProfileForm
│   ├── urls.py           # User URLs
│   ├── tests.py          # 17 tests
│   └── migrations/
├── templates/
│   ├── base.html         # Base template with navbar
│   ├── resources/        # Resource templates
│   │   ├── home.html
│   │   ├── resource_list.html
│   │   ├── resource_detail.html
│   │   ├── add_resource.html
│   │   └── partials/     # HTMX partials
│   ├── users/            # User templates
│   │   ├── profile.html
│   │   └── edit_profile.html
│   └── registration/     # Auth templates
├── static/css/styles.css # Custom styles (CSS variables)
├── media/                # Uploaded files (gitignored)
├── seed_data.py          # Sample resource data
├── seed_files.py         # Sample file uploads
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── manage.py
```

## Key URLs

| Path | Description |
|------|-------------|
| `/` | Home page with stats & recent resources |
| `/resources/` | Resource library with search/filter |
| `/resources/add/` | Add new resource (login required) |
| `/resources/<pk>/` | Resource detail with preview, comments, upvotes |
| `/resources/<pk>/download/` | Download file or open external link |
| `/resources/<pk>/upvote/` | Upvote resource (HTMX) |
| `/resources/<pk>/comment/` | Add comment (login required) |
| `/users/<username>/` | Public user profile |
| `/users/<username>/follow/` | Follow/unfollow user |
| `/users/edit/` | Edit own profile |
| `/admin/` | Django admin panel |

## Testing

```bash
# Run all tests (36 tests)
python manage.py test

# Run specific app tests
python manage.py test resources
python manage.py test users

# With coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

**Current coverage**: 36 tests passing (19 resources + 17 users)

## Deployment

### Docker
```bash
docker-compose up --build
```

### Manual (Production)
```bash
# On server
export DEBUG=False
export SECRET_KEY=<strong-secret>
export DATABASE_URL=<supabase-url>
export ALLOWED_HOSTS=yourdomain.com

python manage.py migrate
python manage.py collectstatic --noinput

# Run with gunicorn
gunicorn campus_hub.wsgi:application --bind 0.0.0.0:8000
```

### Supabase (PostgreSQL)
1. Create Supabase project
2. Get connection string from Settings → Database
3. Add to `.env` as `DATABASE_URL`
4. Run `python manage.py migrate`

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Django 4.2 |
| Database | PostgreSQL (Supabase) / SQLite (dev) |
| Frontend | Bootstrap 5, HTMX, Vanilla JS |
| File Storage | Local / Cloudinary / AWS S3 |
| Containerization | Docker, Docker Compose |
| Testing | Django TestCase, Client |

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Django community for the excellent framework
- HTMX for enabling dynamic UX without SPA complexity
- Supabase for managed PostgreSQL
- Bootstrap for responsive UI components

---

**Built with ❤️ for students, by students**
**MADE BY SIDDHARTHA TRIPATHY**