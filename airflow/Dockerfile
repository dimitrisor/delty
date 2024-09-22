FROM apache/airflow:2.10.2

USER root

RUN apt-get update && apt-get install -y git curl && apt-get clean

COPY ./requirements.txt ./airflow/requirements.txt

USER airflow

RUN pip install --upgrade pip && \
    pip install -r ./airflow/requirements.txt

ENTRYPOINT ["/usr/bin/dumb-init", "--"]


WORKDIR /opt/airflow

# Set the command
CMD ["/bin/bash", "-c", "/opt/airflow/wait-for-db.sh db && \
    airflow db migrate && \
    sleep 20 && \
    airflow users create --username 'admin' --password 'admin' --firstname '' --lastname '' --role Admin --email '' && \
    airflow webserver -p 8080 & airflow scheduler"]
