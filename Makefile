start:
	awslocal s3 mb s3://selected-element-html-s3-bucket
	poetry run python manage.py migrate
	poetry run python manage.py runserver 8000

start-worker:
	poetry run python manage.py rundramatiq

load-fixtures:
	poetry run python manage.py migrate
	poetry run python manage.py fill_db_with_initial_data

test:
	poetry run python pytest
