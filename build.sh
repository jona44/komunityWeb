#!/usr/bin/env bash
# Render build script — runs before the web service starts
set -o errexit

pip install -r requirements.txt

# Build Tailwind CSS
cd theme/static_src
npm ci
npm run build
cd ../..

# Collect static files (WhiteNoise serves them)
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate
