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

# Setup cron job
# 1) Install cron
# 2) Create logging file
# 3) Write the cron command
# 4) Give execution rights on the cron job
# 5) Add cron job to crontab
# 6) Install postgresql-client to use pg_isready
RUN apt-get update && apt-get install -y cron bash postgresql-client
RUN touch /var/log/cron.log
RUN echo "*/1 * * * * cd /app && export $(cat /app/.env | xargs) DJANGO_SETTINGS_MODULE='app.settings.local' && /usr/local/bin/poetry run python /app/manage.py track_element_diff >> /var/log/cron.log 2>&1" > /etc/cron.d/mycron
RUN chmod 0644 /etc/cron.d/mycron
RUN crontab /etc/cron.d/mycron
