FROM apache/airflow:2.2.4
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         git \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER airflow
COPY webserver_config.py /opt/airflow/
COPY user_auth.py /home/airflow/.local/lib/python3.7/site-packages/airflow/api/auth/backend
RUN  pip install airflow-code-editor black
RUN pip install 'apache-airflow[amazon]'
RUN pip install 'apache-airflow[sendgrid]'
RUN pip install jupyter-repo2docker