"""Notification channel handlers using strategy pattern."""

from abc import ABC, abstractmethod
import json
import logging
from typing import Dict, Any
import requests

logger = logging.getLogger(__name__)


class NotificationHandler(ABC):
    """Abstract base class for notification handlers."""
    
    @abstractmethod
    def send(self, config: Dict[str, Any], message: str, **kwargs) -> bool:
        """
        Send a notification through the channel.
        
        Args:
            config: Channel configuration dictionary
            message: Rendered message to send
            **kwargs: Additional parameters
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass


class SlackHandler(NotificationHandler):
    """Handler for Slack webhook notifications."""
    
    def send(self, config: Dict[str, Any], message: str, **kwargs) -> bool:
        """Send notification to Slack via webhook."""
        try:
            webhook_url = config.get("webhook_url")
            if not webhook_url:
                logger.error("Slack webhook_url not configured")
                return False
            
            payload = {
                "text": message,
                "username": config.get("username", "Airflow Notification"),
                "icon_emoji": config.get("icon_emoji", ":airflow:"),
            }
            
            response = requests.post(
                webhook_url,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("Slack notification sent successfully")
                return True
            else:
                logger.error(f"Slack notification failed: {response.status_code} - {response.text}")
                return False
        
        except Exception as e:
            logger.error(f"Error sending Slack notification: {str(e)}")
            return False


class SMSHandler(NotificationHandler):
    """Handler for SMS notifications."""
    
    def send(self, config: Dict[str, Any], message: str, **kwargs) -> bool:
        """Send SMS notification."""
        try:
            api_url = config.get("api_url")
            api_key = config.get("api_key")
            phone_number = kwargs.get("phone_number")
            
            if not all([api_url, api_key, phone_number]):
                logger.error("SMS configuration incomplete")
                return False
            
            payload = {
                "to": phone_number,
                "message": message,
            }
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            
            response = requests.post(
                api_url,
                json=payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                logger.info(f"SMS sent successfully to {phone_number}")
                return True
            else:
                logger.error(f"SMS failed: {response.status_code} - {response.text}")
                return False
        
        except Exception as e:
            logger.error(f"Error sending SMS: {str(e)}")
            return False


class YouduHandler(NotificationHandler):
    """Handler for Youdu (有度) webhook notifications."""
    
    def send(self, config: Dict[str, Any], message: str, **kwargs) -> bool:
        """Send notification to Youdu via webhook."""
        try:
            webhook_url = config.get("webhook_url")
            app_id = config.get("app_id")
            
            if not webhook_url:
                logger.error("Youdu webhook_url not configured")
                return False
            
            payload = {
                "toUser": kwargs.get("user_id", ""),
                "msgType": "text",
                "text": {
                    "content": message
                }
            }
            
            if app_id:
                payload["agentId"] = app_id
            
            response = requests.post(
                webhook_url,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("Youdu notification sent successfully")
                return True
            else:
                logger.error(f"Youdu notification failed: {response.status_code} - {response.text}")
                return False
        
        except Exception as e:
            logger.error(f"Error sending Youdu notification: {str(e)}")
            return False


class FCMHandler(NotificationHandler):
    """Handler for Firebase Cloud Messaging (FCM) notifications."""
    
    def send(self, config: Dict[str, Any], message: str, **kwargs) -> bool:
        """Send push notification via FCM."""
        try:
            server_key = config.get("server_key")
            device_token = kwargs.get("device_token")
            
            if not all([server_key, device_token]):
                logger.error("FCM configuration incomplete")
                return False
            
            fcm_url = "https://fcm.googleapis.com/fcm/send"
            
            payload = {
                "to": device_token,
                "notification": {
                    "title": kwargs.get("title", "Airflow Notification"),
                    "body": message,
                },
                "data": kwargs.get("data", {}),
            }
            
            headers = {
                "Authorization": f"key={server_key}",
                "Content-Type": "application/json",
            }
            
            response = requests.post(
                fcm_url,
                json=payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success", 0) > 0:
                    logger.info("FCM notification sent successfully")
                    return True
                else:
                    logger.error(f"FCM notification failed: {result}")
                    return False
            else:
                logger.error(f"FCM request failed: {response.status_code} - {response.text}")
                return False
        
        except Exception as e:
            logger.error(f"Error sending FCM notification: {str(e)}")
            return False


class APNSHandler(NotificationHandler):
    """Handler for Apple Push Notification Service (APNS).
    
    Note: This is a placeholder implementation. APNS requires more complex 
    setup with certificates and proper authentication. To implement:
    - Use PyAPNs2 or similar library
    - Provide certificate/key files
    - Implement proper authentication flow
    """
    
    def send(self, config: Dict[str, Any], message: str, **kwargs) -> bool:
        """Send push notification via APNS.
        
        This is a placeholder implementation that always returns False.
        Implement proper APNS integration when needed.
        """
        logger.warning("APNS handler not fully implemented yet")
        raise NotImplementedError(
            "APNS support requires additional implementation. "
            "See handler docstring for requirements."
        )


# Handler registry
HANDLERS = {
    "slack": SlackHandler(),
    "sms": SMSHandler(),
    "youdu": YouduHandler(),
    "fcm": FCMHandler(),
    "apns": APNSHandler(),
}


def get_handler(channel_type: str) -> NotificationHandler:
    """Get the appropriate handler for a channel type."""
    return HANDLERS.get(channel_type.lower())
