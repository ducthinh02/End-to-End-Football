import pendulum
from airflow.decorators import dag, task
from datetime import datetime,timedelta

from airflow.providers.standard.operators.bash import BashOperator

@dag(
    dag_id="dbt_transform_pipeline",
    schedule=None,
    start_date=pendulum.datetime(2026,8,20, tz="Asia/Ho_Chi_Minh"),
    catchup=False,
    max_active_runs=1,       

    tags=["dbt","transformation"],
)
def dbt_football_pipeline():
    
    dbt_run = BashOperator(
        task_id="dbt_run_module",
        bash_command=("cd /usr/app && "
                      "export DBT_ALLOW_EXPERIMENTAL_ADAPTERS=true && "
                      "dbt --log-path /tmp/dbt_logs run --profiles-dir /usr/app/profiles --target-path /tmp/dbt_target --debug")                    
    )
    # --log-path /tmp/dbt_logs
    dbt_test= BashOperator(
        task_id="dbt_test_module",
        bash_command=("cd /usr/app && "
                      "export DBT_ALLOW_EXPERIMENTAL_ADAPTERS=true && "
                      "dbt --log-path /tmp/dbt_logs test --profiles-dir /usr/app/profiles --target-path /tmp/dbt_target --debug")
    )
    
    dbt_run>>dbt_test
    
    # check_dbt_task = BashOperator(
    # task_id="check_dbt_installed",
    # bash_command="pip list",
    # )   
    # check_dbt_task
    
    # dbt_run = BashOperator(
    #     task_id="dbt_run_module",
    #     bash_command=(
    #         "echo '--- THƯ MỤC HIỆN TẠI ---' && pwd && "
    #         "echo '--- NỘI DUNG /usr/app ---' && ls -la /usr/app && "
    #         "cd /usr/app && dbt run --profiles-dir /root/.dbt"
    #     ),
    # )
    # dbt_run
dbt_football_pipeline()