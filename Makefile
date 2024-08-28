start:
	poetry run python manage.py migrate
	poetry run python manage.py runserver 8000

start-worker:
	poetry run python manage.py rundramatiq

install:
	poetry run python manage.py migrate
	playwright install
	poetry run python manage.py fill_db_with_initial_data

test:
	poetry run python manage.py test delty/tests
