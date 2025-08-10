#!/bin/bash
set -e

echo "Starting Django application..."

# Run migrations
echo "Running migrations..."
uv run manage.py migrate --no-input

# Collect static files (if needed)
# echo "Collecting static files..."
# uv run manage.py collectstatic --no-input

# Create superuser if it doesn't exist
echo "Creating superuser if needed..."
uv run manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    print('Creating admin user...')
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Admin user created successfully!')
else:
    print('Admin user already exists.')
"

# Start the application
echo "Starting Gunicorn..."
exec uv run gunicorn --bind 0.0.0.0:8000 --workers 2 --timeout 120 movie_rec_project.wsgi:application
