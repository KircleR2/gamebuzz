#!/usr/bin/env bash
# exit on error
set -o errexit
set -x

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
python manage.py collectstatic --no-input --clear

# Verify static files were collected
if [ -f "staticfiles/css/gamebuzz.css" ]; then
    echo "✅ gamebuzz.css successfully collected to staticfiles/css/gamebuzz.css"
else
    echo "❌ ERROR: gamebuzz.css NOT found in staticfiles/css/"
    # List static directory to debug
    echo "Contents of static/:"
    ls -R static/
    echo "Contents of staticfiles/:"
    ls -R staticfiles/
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
