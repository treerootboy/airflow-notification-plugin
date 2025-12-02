"""Database initialization utilities."""

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from airflow.settings import Session as AirflowSession

from airflow_notification_plugin.models import Base

logger = logging.getLogger(__name__)


def init_db():
    """Initialize database tables."""
    try:
        # Use Airflow's database session
        session = AirflowSession()
        engine = session.get_bind()
        
        # Create all tables
        Base.metadata.create_all(engine)
        
        logger.info("Notification plugin tables created successfully")
        session.close()
        
        return True
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        return False


def create_default_templates():
    """Create default notification templates."""
    from airflow_notification_plugin.models import (
        NotificationTemplate,
        EventType,
        ChannelType,
    )
    
    try:
        session = AirflowSession()
        
        # Default templates for each event type and channel type combination
        default_templates = [
            {
                "name": "default_task_success_slack",
                "event_type": EventType.TASK_SUCCESS,
                "channel_type": ChannelType.SLACK,
                "template_content": "✅ *Task Succeeded*\n*DAG:* {{ dag_id }}\n*Task:* {{ task_id }}\n*Execution Date:* {{ execution_date }}\n*Duration:* {{ duration }}s",
                "description": "Default Slack template for task success",
            },
            {
                "name": "default_task_failed_slack",
                "event_type": EventType.TASK_FAILED,
                "channel_type": ChannelType.SLACK,
                "template_content": "❌ *Task Failed*\n*DAG:* {{ dag_id }}\n*Task:* {{ task_id }}\n*Execution Date:* {{ execution_date }}\n*Try Number:* {{ try_number }}/{{ max_tries }}",
                "description": "Default Slack template for task failure",
            },
            {
                "name": "default_task_success_sms",
                "event_type": EventType.TASK_SUCCESS,
                "channel_type": ChannelType.SMS,
                "template_content": "Task {{ task_id }} in DAG {{ dag_id }} succeeded",
                "description": "Default SMS template for task success",
            },
            {
                "name": "default_task_failed_sms",
                "event_type": EventType.TASK_FAILED,
                "channel_type": ChannelType.SMS,
                "template_content": "Task {{ task_id }} in DAG {{ dag_id }} failed",
                "description": "Default SMS template for task failure",
            },
        ]
        
        for template_data in default_templates:
            # Check if template already exists
            existing = session.query(NotificationTemplate).filter_by(
                name=template_data["name"]
            ).first()
            
            if not existing:
                template = NotificationTemplate(**template_data)
                session.add(template)
        
        session.commit()
        logger.info("Default templates created successfully")
        session.close()
        
        return True
    except Exception as e:
        logger.error(f"Error creating default templates: {str(e)}")
        return False


if __name__ == "__main__":
    # Initialize database when run as script
    init_db()
    create_default_templates()
