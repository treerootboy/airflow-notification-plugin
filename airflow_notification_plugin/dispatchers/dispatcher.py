"""Main notification dispatcher hub."""

import json
import logging
from typing import Dict, Any, List
from jinja2 import Template, TemplateError
from sqlalchemy.orm import Session
from airflow.settings import Session as AirflowSession

from airflow_notification_plugin.models import (
    DagSubscription,
    NotificationChannel,
    NotificationTemplate,
    DeviceRegistration,
    EventType,
)
from airflow_notification_plugin.dispatchers.handlers import get_handler

logger = logging.getLogger(__name__)


class NotificationDispatcher:
    """Central dispatcher for notifications."""
    
    def __init__(self):
        self.session = AirflowSession()
    
    def dispatch(self, event_type: EventType, event_data: Dict[str, Any]) -> None:
        """
        Dispatch notifications for a given event.
        
        Args:
            event_type: Type of event that occurred
            event_data: Event metadata (dag_id, task_id, state, etc.)
        """
        try:
            dag_id = event_data.get("dag_id")
            
            if not dag_id:
                logger.warning("No dag_id in event data, skipping notification")
                return
            
            # Query subscriptions for this DAG and event type
            subscriptions = self.session.query(DagSubscription).filter(
                DagSubscription.dag_id == dag_id,
                DagSubscription.event_type == event_type,
                DagSubscription.is_active == True
            ).all()
            
            if not subscriptions:
                logger.debug(f"No active subscriptions for {dag_id} / {event_type.value}")
                return
            
            logger.info(f"Found {len(subscriptions)} subscriptions for {dag_id} / {event_type.value}")
            
            # Process each subscription
            for subscription in subscriptions:
                try:
                    self._send_notification(subscription, event_type, event_data)
                except Exception as e:
                    logger.error(f"Error processing subscription {subscription.id}: {str(e)}")
        
        except Exception as e:
            logger.error(f"Error dispatching notifications: {str(e)}")
        finally:
            self.session.close()
    
    def _send_notification(
        self,
        subscription: DagSubscription,
        event_type: EventType,
        event_data: Dict[str, Any]
    ) -> None:
        """Send notification for a specific subscription."""
        try:
            channel = subscription.channel
            
            if not channel or not channel.is_active:
                logger.warning(f"Channel {subscription.channel_id} is not active")
                return
            
            # Get or create default template
            template = self._get_template(event_type, channel.channel_type)
            
            if not template:
                logger.warning(f"No template found for {event_type.value} / {channel.channel_type.value}")
                return
            
            # Render message from template
            message = self._render_template(template.template_content, event_data)
            
            if not message:
                logger.error("Failed to render message template")
                return
            
            # Parse channel config
            try:
                config = json.loads(channel.config)
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON config for channel {channel.id}")
                return
            
            # Get appropriate handler
            handler = get_handler(channel.channel_type.value)
            
            if not handler:
                logger.error(f"No handler found for channel type {channel.channel_type.value}")
                return
            
            # Prepare additional kwargs
            kwargs = {
                "user_id": subscription.user_id,
                "dag_id": event_data.get("dag_id"),
                "task_id": event_data.get("task_id"),
            }
            
            # For push notifications, get device tokens
            if channel.channel_type.value in ["fcm", "apns"]:
                devices = self._get_user_devices(
                    subscription.user_id,
                    channel.channel_type.value
                )
                
                for device in devices:
                    kwargs["device_token"] = device.device_token
                    success = handler.send(config, message, **kwargs)
                    
                    if success:
                        logger.info(f"Notification sent to device {device.id}")
                    else:
                        logger.warning(f"Failed to send notification to device {device.id}")
            else:
                # Send to channel (Slack, SMS, Youdu)
                success = handler.send(config, message, **kwargs)
                
                if success:
                    logger.info(f"Notification sent via {channel.name}")
                else:
                    logger.warning(f"Failed to send notification via {channel.name}")
        
        except Exception as e:
            logger.error(f"Error sending notification: {str(e)}")
    
    def _get_template(self, event_type: EventType, channel_type) -> NotificationTemplate:
        """Get notification template for event and channel type."""
        template = self.session.query(NotificationTemplate).filter(
            NotificationTemplate.event_type == event_type,
            NotificationTemplate.channel_type == channel_type,
            NotificationTemplate.is_active == True
        ).first()
        
        # If no specific template, use a default one
        if not template:
            template = self._get_default_template(event_type)
        
        return template
    
    def _get_default_template(self, event_type: EventType) -> NotificationTemplate:
        """Create a default in-memory template."""
        default_templates = {
            EventType.TASK_SUCCESS: "✅ Task {{ task_id }} in DAG {{ dag_id }} succeeded at {{ execution_date }}",
            EventType.TASK_FAILED: "❌ Task {{ task_id }} in DAG {{ dag_id }} failed at {{ execution_date }}",
            EventType.TASK_RETRY: "🔄 Task {{ task_id }} in DAG {{ dag_id }} is retrying at {{ execution_date }}",
            EventType.SLA_MISS: "⏰ SLA missed for task {{ task_id }} in DAG {{ dag_id }}",
            EventType.DAG_SUCCESS: "✅ DAG {{ dag_id }} completed successfully at {{ execution_date }}",
            EventType.DAG_FAILED: "❌ DAG {{ dag_id }} failed at {{ execution_date }}",
        }
        
        # Create temporary template object
        template = NotificationTemplate(
            name=f"default_{event_type.value}",
            event_type=event_type,
            channel_type=None,  # Generic
            template_content=default_templates.get(event_type, "Event occurred: {{ dag_id }}")
        )
        
        return template
    
    def _render_template(self, template_content: str, context: Dict[str, Any]) -> str:
        """Render Jinja2 template with context."""
        try:
            template = Template(template_content)
            return template.render(**context)
        except TemplateError as e:
            logger.error(f"Template rendering error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error rendering template: {str(e)}")
            return None
    
    def _get_user_devices(self, user_id: str, platform_type: str) -> List[DeviceRegistration]:
        """Get active devices for a user and platform."""
        devices = self.session.query(DeviceRegistration).filter(
            DeviceRegistration.user_id == user_id,
            DeviceRegistration.platform_type.has(value=platform_type),
            DeviceRegistration.is_active == True
        ).all()
        
        return devices


# Global dispatcher instance
dispatcher = NotificationDispatcher()
