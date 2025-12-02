"""Database models for the notification plugin."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum


Base = declarative_base()


class ChannelType(enum.Enum):
    """Supported notification channel types."""
    SLACK = "slack"
    SMS = "sms"
    YOUDU = "youdu"
    FCM = "fcm"
    APNS = "apns"


class EventType(enum.Enum):
    """Airflow task event types."""
    TASK_SUCCESS = "task_success"
    TASK_FAILED = "task_failed"
    TASK_RETRY = "task_retry"
    SLA_MISS = "sla_miss"
    DAG_SUCCESS = "dag_success"
    DAG_FAILED = "dag_failed"


class PlatformType(enum.Enum):
    """Client platform types."""
    PWA = "pwa"
    IOS = "ios"
    ANDROID = "android"


class NotificationChannel(Base):
    """Model for notification channel configurations."""
    
    __tablename__ = "notification_channel"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    channel_type = Column(Enum(ChannelType), nullable=False)
    config = Column(Text, nullable=False)  # JSON string for channel-specific config
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    subscriptions = relationship("DagSubscription", back_populates="channel")
    
    def __repr__(self):
        return f"<NotificationChannel(name='{self.name}', type='{self.channel_type.value}')>"


class DagSubscription(Base):
    """Model for DAG event subscriptions."""
    
    __tablename__ = "dag_subscription"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(100), nullable=False)
    dag_id = Column(String(250), nullable=False)
    event_type = Column(Enum(EventType), nullable=False)
    channel_id = Column(Integer, ForeignKey("notification_channel.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    channel = relationship("NotificationChannel", back_populates="subscriptions")
    
    def __repr__(self):
        return f"<DagSubscription(user='{self.user_id}', dag='{self.dag_id}', event='{self.event_type.value}')>"


class NotificationTemplate(Base):
    """Model for notification message templates."""
    
    __tablename__ = "notification_template"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    event_type = Column(Enum(EventType), nullable=False)
    channel_type = Column(Enum(ChannelType), nullable=False)
    template_content = Column(Text, nullable=False)  # Jinja2 template
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<NotificationTemplate(name='{self.name}', event='{self.event_type.value}')>"


class DeviceRegistration(Base):
    """Model for client device registrations."""
    
    __tablename__ = "device_registration"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    device_token = Column(String(500), nullable=False, unique=True)
    platform_type = Column(Enum(PlatformType), nullable=False)
    user_id = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    last_used = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<DeviceRegistration(user='{self.user_id}', platform='{self.platform_type.value}')>"
