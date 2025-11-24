web: gunicorn event_platform.wsgi:application --bind 0.0.0.0:${PORT:-8080} --workers 2
release: python manage.py collectstatic --no-input || echo "Warning: collectstatic failed" 