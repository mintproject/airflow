FROM apache/airflow:2.2.4
USER root

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         git \
         ca-certificates \
         curl \
         gnupg \
         lsb-release \
  && curl -fsSL https://download.docker.com/linux/ubuntu/gpg |  gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg \
  && echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null \
  && apt-get update \
  && apt-get install -y --no-install-recommends docker-ce-cli \
  && apt-get install -y --no-install-recommends cwltool \
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
RUN mkdir -p /home/airflow/.cache/cwltool && chown -R default /home/airflow/.cache/cwltool