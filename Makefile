start:
	poetry run python manage.py migrate
	poetry run python manage.py runserver 8000

start-worker:
	poetry run python manage.py rundramatiq

install:
	poetry run python manage.py migrate
	DJANGO_SUPERUSER_USERNAME=admin \
    DJANGO_SUPERUSER_PASSWORD=admin \
	DJANGO_SUPERUSER_EMAIL="" \
    python manage.py createsuperuser --noinput
	playwright install-deps
	playwright install

test:
	poetry run python manage.py test delty/tests
