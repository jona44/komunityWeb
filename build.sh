#!/usr/bin/env bash
# Render build script — runs before the web service starts
set -o errexit

pip install -r requirements.txt

# Build Tailwind CSS
cd theme/static_src
npm ci
npm run build
cd ../..

# Collect static files using production settings so WhiteNoise
# CompressedStaticFilesStorage compresses assets at build time.
# SECRET is provided by Render; fall back to a throwaway value locally.
export DJANGO_SETTINGS_MODULE=core.deployment
export SECRET="${SECRET:-build-phase-placeholder}"
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate
