"""
Example DAG to test the notification plugin.

This DAG includes tasks that will succeed and fail,
triggering notifications based on your subscriptions.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}


def success_task():
    """A task that will succeed."""
    print("This task will succeed and trigger a success notification")
    return "Success!"


def fail_task():
    """A task that will fail."""
    print("This task is about to fail...")
    raise Exception("Intentional failure to trigger notification")


with DAG(
    'notification_test_dag',
    default_args=default_args,
    description='Test DAG for notification plugin',
    schedule_interval=None,  # Manual trigger only
    catchup=False,
    tags=['notification', 'test'],
) as dag:
    
    # Task 1: Will succeed
    task_success = PythonOperator(
        task_id='successful_task',
        python_callable=success_task,
    )
    
    # Task 2: Simple bash task
    task_bash = BashOperator(
        task_id='bash_task',
        bash_command='echo "Running bash task" && sleep 2',
    )
    
    # Task 3: Will fail (commented out by default to avoid breaking the DAG)
    # Uncomment to test failure notifications
    # task_fail = PythonOperator(
    #     task_id='failing_task',
    #     python_callable=fail_task,
    # )
    
    # Set task dependencies
    task_success >> task_bash
    # task_bash >> task_fail  # Uncomment to test failure
