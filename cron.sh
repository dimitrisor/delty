#!/bin/bash

# Ensure the log file exists
touch /var/log/cron.log

# Add the cron job to crontab
echo "*/1 * * * * root export DATABASE_URL='postgres://delty_user:delty_pass@db:5432/delty' && export DJANGO_SETTINGS_MODULE='app.settings.local' && poetry run python /app/manage.py track_element_diff --verbosity 2 >> /var/log/cron.log 2>&1" >> /etc/crontab

# Start the cron daemon
cron

# Wait until the log file is ready before tailing it
while [ ! -f /var/log/cron.log ]; do
    sleep 1
done

# Tail the cron log file to keep the container running
tail -f /var/log/cron.log
