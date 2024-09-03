# Use an official Python runtime as a parent image
FROM python:3.10.5-slim

# Set the working directory in the container
WORKDIR /app

# Copy the project files into the working directory
COPY . /app

# Install Poetry
RUN pip install poetry

# Install dependencies
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

# Install playwright dependencies
RUN playwright install-deps
RUN playwright install

ENV DJANGO_SETTINGS_MODULE="app.settings.local"

## Run migrations
#RUN poetry run python manage.py migrate

# Collect static files
RUN poetry run python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
