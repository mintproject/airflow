
from datetime import datetime, timedelta
from textwrap import dedent
from airflow.models import Param

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
with DAG(
    'n',
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        'depends_on_past': False,
        'email': ['maxiosorio@gmail.com'],
        'email_on_failure': True,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    params={
        "component_name": Param(
            default='name',
            type="string"
        ),
        "url": Param(
            default="https://github.com/mosoriob/MIC_model",
            type="string"
        ),
    },
    description='List notebook from a git repository',
    catchup=False,
    tags=['mic'],
    start_date=datetime(2021, 1, 1),
) as dag:
    
    import os
    t1 = BashOperator(
        task_id="bash_task",
        bash_command="/home/airflow/.local/bin/jupyter-repo2docker  --no-run --image-name mintproject/name:{{ ds_nodash }} --push {{ params.url }} ",
        env={"git_url": '{{ params.url if dag_run else "" }}', "DOCKER_HOST": 'http://socat:8375', "tag": '{{ ds_nodash }}'},
        dag=dag,
    )
    

    t1