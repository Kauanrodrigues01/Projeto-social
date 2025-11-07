#!/bin/bash

# Exit on error
set -e

echo "🚀 Starting Django application..."

# Wait for database using Django management command
echo "⏳ Checking database connection..."
python manage.py wait_for_db --timeout=60

# Run migrations
echo "📦 Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Django application is ready!"

# Execute the main command
exec "$@"
