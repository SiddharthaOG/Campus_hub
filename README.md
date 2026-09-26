<div align="center">
  
# 🎓 Campus Resource Hub

A modern Django-based platform for students to share and discover academic resources (notes, previous year papers, lab manuals, study materials) with social features like upvotes, comments, and user following.

![Django](https://img.shields.io/badge/Django-4.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-36_Passing-brightgreen?style=for-the-badge&logo=github-actions&logoColor=white)
![HTMX](https://img.shields.io/badge/HTMX-Dynamic_UX-336791?style=for-the-badge&logo=htmx&logoColor=white)

### 🚀 Live Demo (MVP)

The application is deployed and running live on Render as an MVP. 

*(Note: As this uses Render's free tier, the server may take up to 60 seconds to "wake up" if it has been inactive.)*

[![Live Demo](https://img.shields.io/badge/Live_Demo-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://campus-hub-23pe.onrender.com/)

**Link:** https://campus-hub-23pe.onrender.com/

</div>

---

### 🧑‍💻 About the Project
This project was built as a technical screening challenge to demonstrate clean architecture, modular Django design, and modern full-stack development practices. It uses a traditional Django server-rendered approach supercharged with HTMX for dynamic UX, without the overhead of a React/Vue SPA.

---

### ✨ Features

#### Core Functionality
- **Resource Library**: Browse, search, and filter academic resources by subject, semester, branch, and type
- **File Previews**: Inline PDF viewer and image previews for uploaded files
- **External Links**: Support for Google Drive, GitHub, and other external resource links
- **Download Tracking**: Automatic download counting

#### Social Features
- **Upvotes**: Reddit-style upvoting on resources with real-time updates (HTMX)
- **Comments**: Threaded comments with auto-filled username for logged-in users
- **User Profiles**: Public profiles showing uploaded resources, bio, branch, year, hosteller status
- **Follow System**: Follow/unfollow users, mutual followers detection
- **Career Upvotes**: Aggregate upvote count across all user's resources

#### Admin & Management
- **Supercharged Admin**: Featured resources toggle, branch/semester/type filters, date hierarchy, bulk actions
- **Resource Ownership**: Track who uploaded each resource
- **File Storage**: Local development, Supabase/PostgreSQL ready, Cloudinary/AWS S3 configurable

---

### 🚀 Quick Start

#### Prerequisites
- Python 3.11+
- PostgreSQL (or use SQLite for local dev)
- Git

#### Installation

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

---

### ⚙️ Configuration

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

---

### 🧪 Testing

```bash
# Run all tests (36 tests)
python manage.py test

# Run specific app tests
python manage.py test resources
python manage.py test users
```
**Current coverage**: 36 tests passing (19 resources + 17 users)

---

### 🐳 Deployment

#### Docker
```bash
docker-compose up --build
```

#### Manual (Production)
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

---

### 🗺️ Key URLs

| Path | Description |
|------|-------------|
| `/` | Home page with stats & recent resources |
| `/resources/` | Resource library with search/filter |
| `/resources/add/` | Add new resource (login required) |
| `/resources/<pk>/` | Resource detail with preview, comments, upvotes |
| `/resources/<pk>/download/` | Download file or open external link |
| `/resources/<pk>/upvote/` | Upvote resource (HTMX) |
| `/users/<username>/` | Public user profile |
| `/users/<username>/follow/` | Follow/unfollow user |
| `/admin/` | Django admin panel |

---

### 🏗️ Project Structure

```text
Campus-Hub/
├── campus_hub/           # Project settings
├── resources/            # Main app (CRUD, search, upvotes, comments)
├── users/                # User profiles & social (Follow, Profile)
├── templates/            # Django Templates (Bootstrap 5 + HTMX)
├── static/css/styles.css # Custom dark-mode CSS variables
├── seed_data.py          # Sample resource data
├── Dockerfile            # Containerization
├── docker-compose.yml    # Local Docker Dev Environment
└── manage.py
```

---

<div align="center">
  
**Built with ❤️ for students, by students**
**MADE BY SIDDHARTHA TRIPATHY**

</div>
