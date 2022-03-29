
from datetime import datetime, timedelta
from textwrap import dedent

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
with DAG(
    'find_notebooks',
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
    description='List notebook from a git repository',
    catchup=False,
    tags=['mic'],
    start_date=datetime(2021, 1, 1),
) as dag:

    # t1, t2 and t3 are examples of tasks created by instantiating operators
    t1 = BashOperator(
        task_id="bash_task",
        bash_command="git clone $git_url git_{{ run_id }}",
        env={"git_url": '{{ dag_run.conf["url"] if dag_run else "" }}'},
    )
    
    t2 = BashOperator(
        task_id="find_notebooks",
        bash_command="git clone $git_url",
    )

    t1
