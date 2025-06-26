# GameBuzz Event Platform

A Django-based gaming events platform that allows users to browse, search, and register for gaming events.

## Features

- Browse events by category
- View featured and popular events
- Detailed event information
- User registration and authentication
- Admin interface for event management

## Local Development Setup

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv event_platform_venv
   source event_platform_venv/bin/activate  # On Windows: event_platform_venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```
   python manage.py migrate
   ```
5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```
   python manage.py runserver
   ```
7. Access the application at http://127.0.0.1:8000/

## Deployment to Render

This project is configured for deployment on [Render](https://render.com/).

### Prerequisites

1. Create a [Render account](https://render.com/)
2. Push your code to a Git repository (GitHub, GitLab, etc.)

### Deployment Steps

1. In your Render dashboard, click "New" and select "Blueprint"
2. Connect your Git repository
3. Render will automatically detect the `render.yaml` configuration
4. Click "Apply" to create the services defined in the configuration
5. Wait for the build and deployment to complete

### Manual Deployment

If you prefer to set up services manually:

1. Create a new PostgreSQL database in Render
2. Create a new Web Service:
   - Connect your Git repository
   - Set the build command to `./build.sh`
   - Set the start command to `gunicorn event_platform.wsgi:application`
   - Add the following environment variables:
     - `DATABASE_URL`: Your PostgreSQL connection string
     - `SECRET_KEY`: A secure random string
     - `DEBUG`: false
     - `ALLOWED_HOSTS`: your-app.onrender.com
     - `DJANGO_SETTINGS_MODULE`: event_platform.settings

## Static Files

Static files are served using WhiteNoise in production. In development, you can run:

```
python -m http.server 8080 --directory staticfiles
```

## License

This project is licensed under the MIT License.

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- pip
- virtualenv (recommended)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/gamebuzz.git
   cd gamebuzz
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv event_platform_venv
   source event_platform_venv/bin/activate  # On Windows: event_platform_venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Load sample data (optional):
   ```bash
   python manage.py setup_hero_events
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

8. Access the site at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## 🎯 Usage Guide

### Admin Interface

1. Access the admin at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
2. Log in with your superuser credentials
3. Manage events, categories, and subscribers

#### Creating Events

1. Go to Events > Add Event
2. Fill in the required fields:
   - Title
   - Description
   - Start/End Date & Time
   - Location Details
   - Category
3. Upload images (featured image, hero image)
4. Set additional options (featured, show in hero)
5. Save the event

#### Managing Categories

1. Go to Categories > Add Category
2. Provide a name, slug (optional), and description
3. Set an icon (uses Bootstrap Icons)
4. Set the display order
5. Save the category

### API Usage

The GameBuzz API provides endpoints for accessing events data:

#### Events Endpoints

- `GET /api/events/` - List all events
- `GET /api/events/{id}/` - Get a specific event
- `GET /api/events/?category={category_slug}` - Filter events by category
- `GET /api/events/?featured=true` - Get featured events

#### Categories Endpoints

- `GET /api/categories/` - List all categories
- `GET /api/categories/{id}/` - Get a specific category

Example API request:
```bash
curl -X GET http://127.0.0.1:8000/api/events/?featured=true
```

## 🎨 Design System

GameBuzz uses a custom design system with consistent components:

### Colors

- Primary Blue: `#0066FF`
- Accent Purple: `#6B46C1`
- Accent Green: `#0B3B2C`
- Gold: `#FFD700`
- Dark Blue: `#161347`
- Gray Scale: from `#F9FAFB` to `#111827`

### Typography

- Primary Font: Inter (sans-serif)
- Heading Sizes: 4rem, 2.5rem, 2rem, 1.5rem, 1.25rem
- Body Text: 1rem, 0.875rem

### Components

- Buttons (primary, outline, text)
- Cards (event, category)
- Navigation (header, footer, mobile menu)
- Hero sections (home, category, featured, popular)
- Forms (newsletter, filters)
- Pagination
- Event grids and lists

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Settings

Key settings can be modified in `event_platform/settings.py`:

- `MEDIA_ROOT` - Directory for user-uploaded files
- `STATIC_ROOT` - Directory for collected static files
- `TIME_ZONE` - Default time zone

## 📊 API Documentation

### Authentication

API endpoints are currently public and don't require authentication.

### Response Format

All API responses are in JSON format:

```json
{
  "count": 10,
  "next": "http://127.0.0.1:8000/api/events/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Epic Gaming Championship 2025",
      "slug": "epic-gaming-championship-2025",
      "description": "...",
      "start_date": "2025-07-15",
      "start_time": "10:00:00",
      "end_date": "2025-07-17",
      "end_time": "18:00:00",
      "location_name": "Convention Center",
      "city": "Los Angeles",
      "state_province": "CA",
      "country": "United States",
      "category": {
        "id": 1,
        "name": "Tournaments",
        "slug": "tournaments"
      },
      "featured_image": "/media/events_images/championship.png",
      "is_featured": true
    },
    // More events...
  ]
}
```

### Pagination

API responses are paginated with 10 items per page by default. Use the `next` and `previous` links to navigate.

### Filtering

Events can be filtered using query parameters:

- `category` - Filter by category slug
- `featured` - Filter featured events (true/false)
- `city` - Filter by city name
- `search` - Search in title and description

## 🧪 Testing

Run tests with:

```bash
python manage.py test
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- Django - The web framework used
- Bootstrap Icons - Icon library
- Google Fonts - Typography 