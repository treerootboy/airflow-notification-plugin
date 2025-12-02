"""Airflow event listeners for task and DAG state changes."""

import logging
from typing import Optional
from airflow.listeners import hookimpl
from airflow.models import TaskInstance, DagRun

from airflow_notification_plugin.models import EventType
from airflow_notification_plugin.dispatchers import dispatcher

logger = logging.getLogger(__name__)


@hookimpl
def on_task_instance_success(previous_state, task_instance: TaskInstance, session):
    """Listener for task success events."""
    try:
        event_data = _extract_task_event_data(task_instance)
        dispatcher.dispatch(EventType.TASK_SUCCESS, event_data)
    except Exception as e:
        logger.error(f"Error in on_task_instance_success listener: {str(e)}")


@hookimpl
def on_task_instance_failed(previous_state, task_instance: TaskInstance, session):
    """Listener for task failure events."""
    try:
        event_data = _extract_task_event_data(task_instance)
        dispatcher.dispatch(EventType.TASK_FAILED, event_data)
    except Exception as e:
        logger.error(f"Error in on_task_instance_failed listener: {str(e)}")


@hookimpl
def on_task_instance_running(previous_state, task_instance: TaskInstance, session):
    """Listener for task running events (for retry detection)."""
    try:
        # Check if this is a retry
        if task_instance.try_number > 1:
            event_data = _extract_task_event_data(task_instance)
            dispatcher.dispatch(EventType.TASK_RETRY, event_data)
    except Exception as e:
        logger.error(f"Error in on_task_instance_running listener: {str(e)}")


@hookimpl
def on_dag_run_success(dag_run: DagRun, msg: str):
    """Listener for DAG run success events."""
    try:
        event_data = _extract_dag_event_data(dag_run)
        dispatcher.dispatch(EventType.DAG_SUCCESS, event_data)
    except Exception as e:
        logger.error(f"Error in on_dag_run_success listener: {str(e)}")


@hookimpl
def on_dag_run_failed(dag_run: DagRun, msg: str):
    """Listener for DAG run failure events."""
    try:
        event_data = _extract_dag_event_data(dag_run)
        dispatcher.dispatch(EventType.DAG_FAILED, event_data)
    except Exception as e:
        logger.error(f"Error in on_dag_run_failed listener: {str(e)}")


def _extract_task_event_data(task_instance: TaskInstance) -> dict:
    """Extract event data from a TaskInstance."""
    return {
        "dag_id": task_instance.dag_id,
        "task_id": task_instance.task_id,
        "execution_date": str(task_instance.execution_date),
        "state": task_instance.state,
        "try_number": task_instance.try_number,
        "max_tries": task_instance.max_tries,
        "start_date": str(task_instance.start_date) if task_instance.start_date else None,
        "end_date": str(task_instance.end_date) if task_instance.end_date else None,
        "duration": task_instance.duration,
        "hostname": task_instance.hostname,
        "log_url": task_instance.log_url if hasattr(task_instance, 'log_url') else None,
    }


def _extract_dag_event_data(dag_run: DagRun) -> dict:
    """Extract event data from a DagRun."""
    return {
        "dag_id": dag_run.dag_id,
        "run_id": dag_run.run_id,
        "execution_date": str(dag_run.execution_date),
        "state": dag_run.state,
        "start_date": str(dag_run.start_date) if dag_run.start_date else None,
        "end_date": str(dag_run.end_date) if dag_run.end_date else None,
        "external_trigger": dag_run.external_trigger,
    }
