"""API endpoints for the notification plugin."""

from airflow_notification_plugin.api.device_registration import device_registration_blueprint

__all__ = ["device_registration_blueprint"]
