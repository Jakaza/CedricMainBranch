# Cedric House Planning Backend

Django REST API backend for the Cedric House Planning React frontend.

## Features

- **Properties Management**: Full CRUD for house plans and built homes
- **Inquiries System**: Contact messages and quote requests
- **Image Upload**: Support for multiple property images
- **Admin Panel**: Complete Django admin interface for content management
- **REST API**: RESTful endpoints for frontend consumption

## Tech Stack

- Django 5.2.8
- Django REST Framework 3.16.1
- Django CORS Headers 4.9.0
- Pillow 12.0.0
- SQLite (default database)

## Setup Instructions

### 1. Create Virtual Environment
```bash
python -m venv venv
```

### 2. Activate Virtual Environment
**Windows:**
```bash
.\venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

### Properties
- `GET /api/properties/` - List all properties
- `GET /api/properties/?category=PLAN` - List house plans
- `GET /api/properties/?category=BUILT` - List built homes
- `GET /api/properties/plans/` - List house plans (custom action)
- `GET /api/properties/built/` - List built homes (custom action)
- `GET /api/properties/{id}/` - Get property details
- `POST /api/properties/` - Create new property (admin)
- `PUT /api/properties/{id}/` - Update property (admin)
- `DELETE /api/properties/{id}/` - Delete property (admin)

### Inquiries
- `GET /api/contact/` - List contact messages
- `POST /api/contact/` - Submit contact message
- `GET /api/quotes/` - List quote requests
- `POST /api/quotes/` - Submit quote request

## Admin Panel

Access the admin panel at `http://localhost:8000/admin/`

### Admin Features:
- **Properties**: Add/edit house plans and built homes with images
- **Contact Messages**: View all contact form submissions
- **Quote Requests**: View all quote requests with full details

## Models

### Property
- title, category (PLAN/BUILT), price
- bedrooms, bathrooms, garage
- floor_area, levels, width, depth
- styles (JSON array)
- features, amenities (JSON arrays)
- is_new, is_popular flags
- description, video_url
- Optional: en_suite, lounges, dining_areas, parking, pet_friendly

### PropertyImage
- Multiple images per property
- Ordered display

### ContactMessage
- name, email, phone, subject, message

### QuoteRequest
- Personal details: full_name, email, phone, city
- Design preferences: preferred_style, bedrooms, bathrooms, other_rooms
- Property details: yard_length, yard_breadth, budget
- description

## CORS Configuration

CORS is enabled for all origins in development. For production, update `CORS_ALLOW_ALL_ORIGINS` in `config/settings.py`.

## Media Files

Uploaded images are stored in the `media/` directory. Make sure this directory is writable.

## Development Notes

- Database: SQLite (default) - suitable for development
- For production: Consider PostgreSQL or MySQL
- Secret key should be changed for production
- DEBUG should be False in production
- Configure ALLOWED_HOSTS for production deployment
