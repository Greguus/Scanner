# Use an official Python runtime as a parent image
FROM python:3.11.5-slim-bookworm

# Set environment variables
ENV PYTHONUNBUFFERED 1
#ENV DJANGO_SETTINGS_MODULE myproject.settings  # Replace 'myproject' with your Django project name

# Create and set the working directory
RUN mkdir /app
WORKDIR /app

# Configure Apache and enable mod_wsgi
RUN apt-get update && apt-get install -y apache2 apache2-dev libapache2-mod-wsgi-py3 postgresql

# Copy the local requirements file to the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app/
COPY . /app/

# Enable necessary Apache modules
RUN a2enmod rewrite
RUN a2enmod wsgi

# Create a virtual host configuration for Apache
COPY apache/scanner.conf /etc/apache2/sites-available/
RUN a2ensite scanner

# Expose port 80 for Apache
EXPOSE 80

# Collect static files and perform Django migrations
RUN python manage.py collectstatic --noinput
#RUN python manage.py migrate

# Start Apache when the container runs
CMD ["apachectl", "-D", "FOREGROUND"]
