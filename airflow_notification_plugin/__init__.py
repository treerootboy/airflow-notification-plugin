"""
Airflow Notification Plugin - A comprehensive notification management system for Apache Airflow.

This plugin provides:
- Multi-channel notification support (Slack, SMS, Youdu, FCM, APNS)
- Subscription management for DAG events
- Flask-Admin UI for configuration
- Event listeners for task status changes
- Device registration for mobile/PWA clients
"""

__version__ = "0.1.0"

from airflow.plugins_manager import AirflowPlugin
from flask import Blueprint
from flask_admin import BaseView

from airflow_notification_plugin.views import (
    NotificationChannelView,
    DagSubscriptionView,
    NotificationTemplateView,
    DeviceRegistrationView,
)
from airflow_notification_plugin.api.device_registration import device_registration_blueprint


class NotificationHubView(BaseView):
    """Notification Hub landing page in Airflow UI."""
    
    default_view = "index"
    
    @property
    def category(self):
        return "Notification Hub"
    
    def is_visible(self):
        return True


notification_plugin = Blueprint(
    "notification_plugin",
    __name__,
    template_folder="templates",
    static_folder="static",
)


class AirflowNotificationPlugin(AirflowPlugin):
    """Main plugin class to integrate with Airflow."""
    
    name = "notification_hub"
    
    # Flask blueprints for API endpoints
    flask_blueprints = [device_registration_blueprint]
    
    # Admin views for management UI
    admin_views = [
        NotificationChannelView,
        DagSubscriptionView,
        NotificationTemplateView,
        DeviceRegistrationView,
    ]
    
    # Airflow listeners (registered separately)
    listeners = []
