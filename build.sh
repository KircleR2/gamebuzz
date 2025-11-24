#!/usr/bin/env bash
# exit on error
set -o errexit
set -x

# Force rebuild - timestamp: 2025-11-21-02:30:00
# Set Django settings module
export DJANGO_SETTINGS_MODULE=event_platform.settings

# Install dependencies
pip install -r requirements.txt

# Create media directories
mkdir -p media/events_images
mkdir -p media/events_hero_images
mkdir -p media/organizer_logos
chmod -R 755 media

# Collect static files
# Ensure staticfiles directory exists
mkdir -p staticfiles
echo "Collecting static files..."
echo "STATIC_ROOT will be: $(python -c 'import os; from pathlib import Path; BASE_DIR = Path(__file__).resolve().parent.parent; print(BASE_DIR / "staticfiles")')"
python manage.py collectstatic --no-input --clear --verbosity=2

# Verify static files were collected
echo "Verifying static files collection..."
if [ -f "staticfiles/css/gamebuzz.css" ]; then
    echo "✅ gamebuzz.css successfully collected to staticfiles/css/gamebuzz.css"
    ls -lh staticfiles/css/gamebuzz.css
else
    echo "❌ ERROR: gamebuzz.css NOT found in staticfiles/css/"
    echo "Current directory: $(pwd)"
    echo "Contents of static/:"
    ls -R static/ || echo "static/ directory not found"
    echo "Contents of staticfiles/:"
    ls -R staticfiles/ || echo "staticfiles/ directory not found"
    echo "Checking STATIC_ROOT..."
    python -c "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_platform.settings'); import django; django.setup(); from django.conf import settings; print(f'STATIC_ROOT: {settings.STATIC_ROOT}'); import os; print(f'Exists: {os.path.exists(settings.STATIC_ROOT)}')"
    exit 1
fi

# Run migrations (safe to run in build if DB is accessible, otherwise move to run command or job)
# On DigitalOcean App Platform, build phase might not have DB access if DB is a component in the same app
# and not yet provisioned, but usually it's fine for updates.
# However, standard practice is to run migrations on release/deploy.
# We will keep it here as per user's setup, but robustify it.
echo "Running migrations..."
python manage.py migrate --no-input || echo "⚠️ Warning: Migrations failed during build. This might be expected if DB is not reachable. Please ensure migrations run during deployment."

# Fix media permissions
python manage.py fix_media_permissions || true
