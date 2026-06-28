# Freelance Marketplace Application

## Overview

The Freelance Marketplace is a full-stack web application built with Python, Flask, and Django. It connects freelancers with clients, enabling them to browse services, make bookings, leave reviews, and manage their profiles.

### Key Features

- **User Authentication**: Firebase-based authentication in Flask API, Django built-in auth for web app
- **Freelancer Profiles**: Create profiles, list services, manage bookings
- **Client Services**: Browse services by category/price, book gigs, leave reviews
- **Admin Panel**: Manage users, services, bookings, and reviews
- **Image Uploads**: Profile images and service images with Pillow
- **Responsive Design**: Bootstrap-based responsive UI
- **RESTful API**: Flask API with external API consumption (JSONPlaceholder)



## Installation & Setup

### Prerequisites

- Python 3.8+
- pip
- PostgreSQL (optional, SQLite can be used locally)
- virtualenv

### Flask API Setup

1. **Navigate to Flask directory:**

   ```bash
   cd flask_api
   ```

2. **Create virtual environment:**

   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables:**

   ```bash
   cp .env.example .env
   # Edit .env and add your Firebase credentials
   ```

5. **Run Flask app:**
   ```bash
   python run.py
   ```

   - API available at: `http://localhost:5000`

### Django Web App Setup

1. **Navigate to Django directory:**

   ```bash
   cd django_app
   ```

2. **Create virtual environment:**

   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables:**

   ```bash
   cp .env.example .env
   # Edit .env if using PostgreSQL
   ```

5. **Apply migrations:**

   ```bash
   python manage.py migrate
   ```

6. **Create superuser (admin):**

   ```bash
   python manage.py createsuperuser
   # Username: admin
   # Password: admin1234
   # Email: admin@example.com
   ```

7. **Run Django app:**
   ```bash
   python manage.py runserver
   ```

   - Web app available at: `http://localhost:8000`
   - Admin panel: `http://localhost:8000/admin`

## Usage

### Flask API

#### Available Endpoints

**Public:**

- `GET /` - Home page
- `GET /auth/login` - Login form
- `POST /auth/login` - Submit login
- `GET /auth/signup` - Signup form
- `POST /auth/signup` - Submit signup
- `GET /auth/reset` - Password reset form
- `POST /auth/reset` - Submit reset request


**Protected:**

- `GET /api/services` - Fetch services from external API
- `GET /api/users` - Fetch users from external API
- `POST /api/register` - Register user (JSON)
- `POST /api/login` - Login user (JSON)
- `GET /api/profile` - Get authenticated user profile
- `GET /api/jobs/<id>` - Get job details
- `POST /api/jobs` - Create job posting

### Django Web App

#### Main Views

**Public:**

- `/` - Homepage with stats and featured services
- `/services/` - Browse all services with filters
- `/services/<id>/` - Service details and booking

**Authenticated:**

- `/profile/<user_id>/` - User profile view
- `/services/create/` - Post new service (freelancer only)
- `/services/<id>/edit/` - Edit service (owner only)
- `/services/<id>/delete/` - Delete service (owner only)
- `/bookings/` - My bookings list
- `/bookings/create/<service_id>/` - Book a service
- `/bookings/<id>/cancel/` - Cancel booking
- `/reviews/create/<booking_id>/` - Leave review (client only)

**Admin:**

- `/admin/` - Admin dashboard

## Testing

### Test Credentials

**Django Admin:**

- Username: `admin`
- Password: `admin1234`
- Email: `admin@example.com`

**Firebase (Flask):**

- Email: `test@example.com`
- Password: `test1234`

### Running Tests

```bash
# Django tests
cd django_app
python manage.py test marketplace

# Flask tests (manual with Postman)
# See postman_collection.json for detailed test cases
```

### Postman Testing

1. Import `postman_collection.json` into Postman
2. Set environment variables:
   - `base_url`: `http://localhost:5000`
   - `token`: Your Firebase token
3. Run the collections to test all endpoints

## Database Models

### Django Models

**UserProfile**

- One-to-one with Django User
- Stores bio, profile image, user type (freelancer/client), hourly rate, rating, verification status

**Service**

- Belongs to freelancer (UserProfile)
- Has many bookings and reviews
- Fields: title, description, category, price, image, delivery time, rating

**Booking**

- Links service + client + freelancer
- Status: pending, accepted, in_progress, completed, cancelled
- Tracks total price and messages

**Review**

- One-to-one with Booking
- Stores rating (1-5) and comment
- Unique constraint: one review per booking

## API Response Format

### Success Response

```json
{
  "status": "success",
  "data": {
    /* response data */
  },
  "message": "Operation successful"
}
```

### Error Response

```json
{
  "status": "error",
  "data": { "error": "Error description" }
}
```

### GitHub repo link
[link to the repo](https://github.com/DaK-code/Freelance-marketplace.git)
