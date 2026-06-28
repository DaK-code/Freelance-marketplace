# Freelance Marketplace - Quick Start Guide

## 5-Minute Setup

### Prerequisites
- Python 3.8+
- pip & virtualenv

### Flask API (Port 5000)

```bash
cd flask_api
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env
python run.py
```

**Access:** http://localhost:5000

### Django Web App (Port 8000)

```bash
cd django_app
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser  # admin / admin1234
python manage.py runserver
```

**Access:** http://localhost:8000  
**Admin:** http://localhost:8000/admin

---

##  What's Included

###  Complete Features

**Flask API:**
-  User authentication (Firebase-ready)
-  External API integration (JSONPlaceholder)
-  RESTful endpoints with proper error handling
-  Bootstrap-styled templates
-  Session & token-based auth

**Django Web App:**
-  User profiles (freelancer/client)
-  Service listings with filtering
-  Booking system
-  Review & rating system
-  Image uploads
-  Admin panel
-  Responsive UI with Bootstrap 5

###  File Structure

**Core Files:**
- `models.py` - 4 main models (UserProfile, Service, Booking, Review)
- `views.py` - 15+ view functions with full CRUD
- `forms.py` - 6 forms with validation
- `admin.py` - Admin configuration
- `settings.py` - Django configuration

**Templates:**
- `base.html` - Master template
- `home.html` - Homepage
- `service_list.html` - Service browsing
- `service_detail.html` - Service details
- `profile.html` - User profile
- `booking_*` - Booking forms
- `review_form.html` - Review submission

---

##  Default Credentials

**Django Admin:**
- Username: `admin`
- Password: `admin1234`

**Firebase (Flask API):**
- Email: `test@example.com`
- Password: `test1234`

---


### Authentication
```
POST /api/register                  # Register user
POST /api/login                     # Login user
GET  /auth/signup                   # Signup page
GET  /auth/login                    # Login page
```

### Protected Endpoints
```
GET  /api/profile                   # Get user profile
GET  /api/jobs/<id>                 # Get job details
POST /api/jobs                      # Create job posting
```

---

##  Database Schema

### Models

**UserProfile**
- User (OneToOne with Django User)
- bio, profile_image, user_type
- hourly_rate, rating, is_verified

**Service**
- freelancer (FK to UserProfile)
- title, description, category
- price, service_image, delivery_time
- status, rating, total_bookings

**Booking**
- service, client, freelancer
- status, total_price, message
- delivery_date

**Review**
- booking (OneToOne)
- reviewer, rating, comment

---

##  Customization

### Change Flask Port
```python
# flask_api/run.py
app.run(host='0.0.0.0', port=3000)  
```

### Change Django Port
```bash
python manage.py runserver 0.0.0.0:3000
```

### Add PostgreSQL
```python
# django_app/.env
DATABASE_URL=postgresql://user:pass@localhost:5432/freelance_db
```

---

##  Common Commands

### Django Management
```bash
# Migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Run tests
python manage.py test marketplace

# Shell (debug)
python manage.py shell

# Collect static files (production)
python manage.py collectstatic
```
