#!/bin/bash

# Deployment script for Phase II Todo Full-Stack Web Application

set -e

echo "Starting deployment process..."

# Environment validation
if [ -z "$ENVIRONMENT" ]; then
    echo "ENVIRONMENT environment variable must be set"
    exit 1
fi

echo "Deploying to $ENVIRONMENT environment"

# Backend deployment
echo "Building backend..."
cd backend
pip install -r requirements.txt
# Add backend build steps here
cd ..

# Frontend deployment
echo "Building frontend..."
cd frontend
npm install
npm run build
cd ..

# Run tests
echo "Running tests..."
python -m pytest tests/ -v

# Deploy to environment
case $ENVIRONMENT in
    "staging")
        echo "Deploying to staging environment..."
        # Add staging deployment commands
        ;;
    "production")
        echo "Deploying to production environment..."
        # Add production deployment commands
        ;;
    *)
        echo "Unknown environment: $ENVIRONMENT"
        exit 1
        ;;
esac

echo "Deployment completed successfully!"