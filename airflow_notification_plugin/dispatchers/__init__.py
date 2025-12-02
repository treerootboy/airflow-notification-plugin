"""Notification dispatchers and handlers."""

from airflow_notification_plugin.dispatchers.dispatcher import dispatcher, NotificationDispatcher
from airflow_notification_plugin.dispatchers.handlers import get_handler

__all__ = ["dispatcher", "NotificationDispatcher", "get_handler"]
