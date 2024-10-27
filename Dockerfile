# Use the official Python 3.9 slim image
FROM python:3.10-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the Docker container
WORKDIR /app

# Install system dependencies
# Update package list and install required system libraries
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    make \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Clone the specific branch of openai-whisper from GitHub
RUN pip install git+https://github.com/openai/whisper.git@25639fc17ddc013d56c594bfbf7644f2185fad84

# Copy the entire Django project into the container
COPY . .

# Set environment variables for Django
ENV DJANGO_SETTINGS_MODULE=backend.settings
ENV PYTHONUNBUFFERED=1

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port that the Django app will run on
EXPOSE 8000

# Run database migrations
RUN python manage.py migrate

# Command to run the Django application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi:application"]
