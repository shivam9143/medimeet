#!/bin/bash

# Set environment variables
PROJECT_DIR="/home/ec2-user/projects/medimeet/medimeet"  # Path to your project
REPO_DIR="/home/ec2-user/projects/medimeet/medimeet.git"  # Path to your bare repo
GUNICORN_SERVICE="gunicorn.service"             # Gunicorn service name
NGINX_SERVICE="nginx.service"                   # Nginx service name
VENV_DIR="$PROJECT_DIR/venv"                    # Path to your Python virtual environment (if still using it)

# Ensure poetry is installed
echo "Checking if Poetry is installed..."
if ! command -v poetry &> /dev/null
then
    echo "Poetry is not installed. Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    export PATH="$HOME/.local/bin:$PATH"  # Add poetry to PATH
fi

# Pull latest code from bare repository
echo "Pulling latest code from bare repository..."
cd "$PROJECT_DIR" || exit
git --git-dir="$REPO_DIR" --work-tree="$PROJECT_DIR" pull origin main

# Install/update dependencies using Poetry (instead of pip)
echo "Installing dependencies using Poetry..."
cd "$PROJECT_DIR" || exit
poetry install --no-interaction

# Run migrations
echo "Applying migrations..."
poetry run python manage.py migrate

# Collect static files
echo "Collecting static files..."
poetry run python manage.py collectstatic --noinput

# Restart Redis
echo "Restarting Redis..."
sudo systemctl restart redis

# Stop Gunicorn
echo "Stopping Gunicorn..."
sudo systemctl stop "$GUNICORN_SERVICE"

# Start Gunicorn with Poetry
echo "Starting Gunicorn using Poetry environment..."
poetry run gunicorn --workers 3 medimeet.wsgi:application --bind 0.0.0.0:8000 &

# Restart NGINX
echo "Restarting Nginx..."
sudo systemctl restart "$NGINX_SERVICE"

# Deployment completed
echo "Deployment completed successfully!"