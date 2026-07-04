#!/usr/bin/env bash
# Build script for production deployment
set -o errexit

# Collect static files using production settings so WhiteNoise
# CompressedStaticFilesStorage compresses assets at build time.
export DJANGO_SETTINGS_MODULE=core.deployment
export SECRET="${SECRET:-build-phase-placeholder}"
python manage.py collectstatic --no-input
