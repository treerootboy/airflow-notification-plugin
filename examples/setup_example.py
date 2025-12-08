"""
Example usage of the Airflow Notification Plugin.

This script demonstrates how to:
1. Initialize the database
2. Create notification channels
3. Set up DAG subscriptions
4. Register devices for push notifications
"""

from datetime import datetime
from airflow_notification_plugin.db_init import init_db, create_default_templates
from airflow_notification_plugin.models import (
    NotificationChannel,
    DagSubscription,
    NotificationTemplate,
    DeviceRegistration,
    ChannelType,
    EventType,
    PlatformType,
)
from airflow.settings import Session as AirflowSession
import json


def setup_example():
    """Set up example configuration."""
    
    print("1. Initializing database...")
    init_db()
    create_default_templates()
    print("   ✓ Database initialized")
    
    session = AirflowSession()
    
    try:
        # Create a Slack channel
        print("\n2. Creating Slack notification channel...")
        slack_channel = NotificationChannel(
            name="example-slack-channel",
            channel_type=ChannelType.SLACK,
            config=json.dumps({
                "webhook_url": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
                "username": "Airflow Notification Bot",
                "icon_emoji": ":rocket:"
            }),
            is_active=True
        )
        
        # Check if it already exists
        existing_slack = session.query(NotificationChannel).filter_by(
            name="example-slack-channel"
        ).first()
        
        if not existing_slack:
            session.add(slack_channel)
            session.commit()
            channel_id = slack_channel.id
            print(f"   ✓ Slack channel created (ID: {channel_id})")
        else:
            channel_id = existing_slack.id
            print(f"   ✓ Slack channel already exists (ID: {channel_id})")
        
        # Create a DAG subscription
        print("\n3. Creating DAG subscription...")
        subscription = DagSubscription(
            user_id="user@example.com",
            dag_id="example_dag",
            event_type=EventType.TASK_FAILED,
            channel_id=channel_id,
            is_active=True
        )
        
        # Check if it already exists
        existing_sub = session.query(DagSubscription).filter_by(
            user_id="user@example.com",
            dag_id="example_dag",
            event_type=EventType.TASK_FAILED
        ).first()
        
        if not existing_sub:
            session.add(subscription)
            session.commit()
            print(f"   ✓ Subscription created (ID: {subscription.id})")
        else:
            print(f"   ✓ Subscription already exists (ID: {existing_sub.id})")
        
        # Create a custom template
        print("\n4. Creating custom notification template...")
        custom_template = NotificationTemplate(
            name="custom-task-failed-slack",
            event_type=EventType.TASK_FAILED,
            channel_type=ChannelType.SLACK,
            template_content="""
🚨 *ALERT: Task Failure Detected*

*DAG:* {{ dag_id }}
*Task:* {{ task_id }}
*Execution Date:* {{ execution_date }}
*State:* {{ state }}
*Try:* {{ try_number }}/{{ max_tries }}
*Duration:* {{ duration }}s

Please investigate immediately!
            """.strip(),
            description="Custom Slack template for task failures with enhanced formatting",
            is_active=True
        )
        
        existing_template = session.query(NotificationTemplate).filter_by(
            name="custom-task-failed-slack"
        ).first()
        
        if not existing_template:
            session.add(custom_template)
            session.commit()
            print(f"   ✓ Custom template created (ID: {custom_template.id})")
        else:
            print(f"   ✓ Custom template already exists (ID: {existing_template.id})")
        
        # Example device registration
        print("\n5. Registering example device...")
        device = DeviceRegistration(
            device_token="example-fcm-token-12345",
            platform_type=PlatformType.PWA,
            user_id="user@example.com",
            is_active=True
        )
        
        existing_device = session.query(DeviceRegistration).filter_by(
            device_token="example-fcm-token-12345"
        ).first()
        
        if not existing_device:
            session.add(device)
            session.commit()
            print(f"   ✓ Device registered (ID: {device.id})")
        else:
            print(f"   ✓ Device already registered (ID: {existing_device.id})")
        
        print("\n" + "="*60)
        print("✅ Example setup completed successfully!")
        print("="*60)
        print("\nNext steps:")
        print("1. Update the Slack webhook URL in the channel configuration")
        print("2. Access Airflow Web UI -> Notification Hub to manage settings")
        print("3. Create your own DAG subscriptions")
        print("4. Test by triggering a DAG that will fail")
        
    except Exception as e:
        print(f"❌ Error during setup: {str(e)}")
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    setup_example()
