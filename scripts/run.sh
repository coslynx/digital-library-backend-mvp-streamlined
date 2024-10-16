#!/bin/bash

# This script runs the Streamlined Digital Library Backend MVP using Docker Compose.
# It ensures a consistent and automated environment for development and deployment.

# Ensure the environment file (.env) exists and contains necessary configuration.
if [ ! -f .env ]; then
  echo "Error: .env file not found. Please create one with the required environment variables."
  exit 1
fi

# Check if Docker Compose is installed.
if ! command -v docker-compose &> /dev/null; then
  echo "Error: Docker Compose is not installed. Please install it before running this script."
  exit 1
fi

# Build and run the Docker Compose services (app and database).
docker-compose up -d

# Check if the Docker Compose services are running successfully.
docker-compose ps | grep "Up" > /dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "Error: Docker Compose services failed to start. Please check the logs for more details."
  exit 1
fi

# Run database migrations to ensure the latest schema is applied.
docker-compose exec app python src/infrastructure/database/migrations/alembic/upgrade head

# Seed the database with initial data for testing and demonstration purposes.
docker-compose exec app python scripts/seed_database.py

# Print a success message to confirm that the MVP is running.
echo "Streamlined Digital Library Backend MVP is running successfully!"