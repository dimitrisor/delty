CREATE USER airflow_user WITH PASSWORD 'airflow_pass';
CREATE DATABASE airflow;
GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow_user;
