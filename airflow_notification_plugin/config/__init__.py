"""Configuration management for the notification plugin."""

import os
from typing import Optional


class NotificationConfig:
    """Configuration settings for the notification plugin."""
    
    # Database settings
    DATABASE_URL = os.getenv(
        "AIRFLOW_NOTIFICATION_DB_URL",
        "sqlite:////tmp/airflow_notifications.db"
    )
    
    # Retry settings
    MAX_RETRY_ATTEMPTS = int(os.getenv("NOTIFICATION_MAX_RETRIES", "3"))
    RETRY_DELAY_SECONDS = int(os.getenv("NOTIFICATION_RETRY_DELAY", "5"))
    
    # Rate limiting to prevent notification storms
    RATE_LIMIT_ENABLED = os.getenv("NOTIFICATION_RATE_LIMIT_ENABLED", "true").lower() == "true"
    MAX_NOTIFICATIONS_PER_MINUTE = int(os.getenv("NOTIFICATION_RATE_LIMIT_PER_MIN", "60"))
    
    # Logging
    LOG_LEVEL = os.getenv("NOTIFICATION_LOG_LEVEL", "INFO")
    
    # Feature flags
    ENABLE_SLACK = os.getenv("NOTIFICATION_ENABLE_SLACK", "true").lower() == "true"
    ENABLE_SMS = os.getenv("NOTIFICATION_ENABLE_SMS", "true").lower() == "true"
    ENABLE_YOUDU = os.getenv("NOTIFICATION_ENABLE_YOUDU", "true").lower() == "true"
    ENABLE_FCM = os.getenv("NOTIFICATION_ENABLE_FCM", "true").lower() == "true"
    ENABLE_APNS = os.getenv("NOTIFICATION_ENABLE_APNS", "false").lower() == "true"
    
    @classmethod
    def get(cls, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get configuration value."""
        return getattr(cls, key, default)
    
    @classmethod
    def is_channel_enabled(cls, channel_type: str) -> bool:
        """Check if a channel type is enabled."""
        channel_map = {
            "slack": cls.ENABLE_SLACK,
            "sms": cls.ENABLE_SMS,
            "youdu": cls.ENABLE_YOUDU,
            "fcm": cls.ENABLE_FCM,
            "apns": cls.ENABLE_APNS,
        }
        return channel_map.get(channel_type.lower(), False)


config = NotificationConfig()
