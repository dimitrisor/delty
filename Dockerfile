# Use an official Python runtime as a parent image
FROM python:3.12.4-slim

# Set the working directory in the container
WORKDIR /app

# Copy the project files into the working directory
COPY . /app

# Install Poetry
# Ensure Poetry is added to PATH
RUN pip install poetry
ENV PATH="/usr/local/bin:$PATH"

# Install dependencies
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

# Install playwright dependencies
RUN playwright install-deps
RUN playwright install

ENV DJANGO_SETTINGS_MODULE="app.settings.local"

# Collect static files
RUN poetry run python manage.py collectstatic --noinput
