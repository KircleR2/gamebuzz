#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Create media directories
mkdir -p media/events_images
mkdir -p media/events_hero_images
mkdir -p media/organizer_logos
chmod -R 755 media

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Fix media permissions
python manage.py fix_media_permissions 