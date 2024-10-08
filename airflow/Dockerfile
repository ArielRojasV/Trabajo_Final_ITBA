FROM apache/airflow:2.10.1
ADD requirements.txt .


USER root
RUN apt-get update


USER airflow
RUN pip3 install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt
