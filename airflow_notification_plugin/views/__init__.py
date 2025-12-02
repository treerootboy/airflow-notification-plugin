"""Flask-Admin views for notification plugin management."""

from flask_admin.contrib.sqla import ModelView
from flask_admin import expose
from wtforms import TextAreaField
from wtforms.widgets import TextArea

from airflow_notification_plugin.models import (
    NotificationChannel,
    DagSubscription,
    NotificationTemplate,
    DeviceRegistration,
)


class NotificationChannelView(ModelView):
    """Admin view for managing notification channels."""
    
    can_create = True
    can_edit = True
    can_delete = True
    
    column_list = ["id", "name", "channel_type", "is_active", "created_at"]
    column_searchable_list = ["name"]
    column_filters = ["channel_type", "is_active"]
    column_editable_list = ["is_active"]
    
    form_columns = ["name", "channel_type", "config", "is_active"]
    form_args = {
        "config": {
            "widget": TextArea(),
            "description": "JSON configuration for the channel (e.g., webhook URL, API keys)",
        }
    }
    
    column_descriptions = {
        "name": "Unique name for this notification channel",
        "channel_type": "Type of notification channel",
        "config": "JSON configuration (e.g., {'webhook_url': 'https://...'})",
        "is_active": "Whether this channel is active",
    }
    
    def __init__(self, session, **kwargs):
        super(NotificationChannelView, self).__init__(
            NotificationChannel,
            session,
            name="Notification Channels",
            category="Notification Hub",
            **kwargs
        )


class DagSubscriptionView(ModelView):
    """Admin view for managing DAG subscriptions."""
    
    can_create = True
    can_edit = True
    can_delete = True
    
    column_list = ["id", "user_id", "dag_id", "event_type", "channel", "is_active"]
    column_searchable_list = ["user_id", "dag_id"]
    column_filters = ["event_type", "is_active", "user_id"]
    column_editable_list = ["is_active"]
    
    form_columns = ["user_id", "dag_id", "event_type", "channel_id", "is_active"]
    
    column_descriptions = {
        "user_id": "User identifier who will receive notifications",
        "dag_id": "DAG ID to monitor",
        "event_type": "Type of event to trigger notification",
        "channel_id": "Notification channel to use",
        "is_active": "Whether this subscription is active",
    }
    
    def __init__(self, session, **kwargs):
        super(DagSubscriptionView, self).__init__(
            DagSubscription,
            session,
            name="DAG Subscriptions",
            category="Notification Hub",
            **kwargs
        )


class NotificationTemplateView(ModelView):
    """Admin view for managing notification templates."""
    
    can_create = True
    can_edit = True
    can_delete = True
    
    column_list = ["id", "name", "event_type", "channel_type", "is_active"]
    column_searchable_list = ["name"]
    column_filters = ["event_type", "channel_type", "is_active"]
    column_editable_list = ["is_active"]
    
    form_columns = ["name", "event_type", "channel_type", "template_content", "description", "is_active"]
    form_args = {
        "template_content": {
            "widget": TextArea(),
            "description": "Jinja2 template. Available variables: dag_id, task_id, execution_date, state, etc.",
        }
    }
    
    column_descriptions = {
        "name": "Unique name for this template",
        "event_type": "Event type this template is for",
        "channel_type": "Channel type this template is for",
        "template_content": "Jinja2 template content",
    }
    
    def __init__(self, session, **kwargs):
        super(NotificationTemplateView, self).__init__(
            NotificationTemplate,
            session,
            name="Notification Templates",
            category="Notification Hub",
            **kwargs
        )


class DeviceRegistrationView(ModelView):
    """Admin view for managing device registrations."""
    
    can_create = False  # Devices register via API
    can_edit = True
    can_delete = True
    
    column_list = ["id", "user_id", "platform_type", "is_active", "last_used", "created_at"]
    column_searchable_list = ["user_id", "device_token"]
    column_filters = ["platform_type", "is_active", "user_id"]
    column_editable_list = ["is_active"]
    
    form_columns = ["user_id", "platform_type", "device_token", "is_active"]
    
    column_descriptions = {
        "device_token": "Device token for push notifications",
        "platform_type": "Platform type (PWA, iOS, Android)",
        "user_id": "User who owns this device",
        "is_active": "Whether this device is active",
    }
    
    def __init__(self, session, **kwargs):
        super(DeviceRegistrationView, self).__init__(
            DeviceRegistration,
            session,
            name="Device Registrations",
            category="Notification Hub",
            **kwargs
        )
