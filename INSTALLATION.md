# Installation Guide

## Prerequisites

- Apache Airflow 2.0.0 or higher
- Python 3.7 or higher
- Access to Airflow's database
- (Optional) Notification service accounts (Slack, SMS provider, FCM, etc.)

## Installation Steps

### 1. Install the Plugin

#### Option A: From Source

```bash
git clone https://github.com/treerootboy/airflow-notification-plugin.git
cd airflow-notification-plugin
pip install -e .
```

#### Option B: Using pip

```bash
pip install airflow-notification-plugin
```

### 2. Initialize Database Tables

Run the database initialization script:

```bash
python -m airflow_notification_plugin.db_init
```

Or use Python:

```python
from airflow_notification_plugin.db_init import init_db, create_default_templates

init_db()
create_default_templates()
```

### 3. Restart Airflow

Restart the Airflow webserver and scheduler to load the plugin:

```bash
# Stop services
airflow webserver stop
airflow scheduler stop

# Start services
airflow webserver -D
airflow scheduler -D
```

### 4. Verify Installation

1. Open the Airflow Web UI
2. Look for "Notification Hub" in the navigation menu
3. You should see the following sub-menus:
   - Notification Channels
   - DAG Subscriptions
   - Notification Templates
   - Device Registrations

### 5. Configure Your First Channel

1. Navigate to **Notification Hub** → **Notification Channels**
2. Click **Create**
3. Fill in the form:
   - **Name**: e.g., `production-slack`
   - **Channel Type**: Select `slack`
   - **Config**: 
     ```json
     {
       "webhook_url": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
       "username": "Airflow Bot",
       "icon_emoji": ":airflow:"
     }
     ```
   - **Is Active**: Check the box
4. Click **Save**

### 6. Create a Subscription

1. Navigate to **Notification Hub** → **DAG Subscriptions**
2. Click **Create**
3. Fill in the form:
   - **User ID**: Your user identifier (e.g., email)
   - **DAG ID**: The DAG you want to monitor
   - **Event Type**: Select the event (e.g., `task_failed`)
   - **Channel ID**: Select the channel you created
   - **Is Active**: Check the box
4. Click **Save**

### 7. Test the Setup

Run the example setup script:

```bash
python examples/setup_example.py
```

Or manually trigger a test DAG:

```bash
# Copy the example DAG to your DAGs folder
cp examples/notification_test_dag.py $AIRFLOW_HOME/dags/

# Trigger the DAG
airflow dags trigger notification_test_dag
```

## Configuration

### Environment Variables

Create a `.env` file or set environment variables:

```bash
# Optional: Custom database URL (defaults to Airflow's database)
export AIRFLOW_NOTIFICATION_DB_URL="postgresql://user:pass@localhost/airflow"

# Retry settings
export NOTIFICATION_MAX_RETRIES=3
export NOTIFICATION_RETRY_DELAY=5

# Rate limiting
export NOTIFICATION_RATE_LIMIT_ENABLED=true
export NOTIFICATION_RATE_LIMIT_PER_MIN=60

# Enable/disable channels
export NOTIFICATION_ENABLE_SLACK=true
export NOTIFICATION_ENABLE_SMS=true
export NOTIFICATION_ENABLE_YOUDU=true
export NOTIFICATION_ENABLE_FCM=true
export NOTIFICATION_ENABLE_APNS=false
```

## Setting Up Notification Channels

### Slack

1. Create a Slack Incoming Webhook:
   - Go to https://api.slack.com/messaging/webhooks
   - Click "Create your Slack app"
   - Follow the instructions to get a webhook URL

2. Add the channel in Airflow UI with config:
   ```json
   {
     "webhook_url": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
     "username": "Airflow Bot",
     "icon_emoji": ":robot_face:"
   }
   ```

### Firebase Cloud Messaging (FCM)

1. Get your FCM Server Key:
   - Go to Firebase Console
   - Project Settings → Cloud Messaging
   - Copy the Server Key

2. Add the channel in Airflow UI with config:
   ```json
   {
     "server_key": "YOUR_FCM_SERVER_KEY"
   }
   ```

3. Register devices using the API:
   ```bash
   curl -X POST http://your-airflow-host/api/v1/notification/register-device \
     -H "Content-Type: application/json" \
     -d '{
       "device_token": "YOUR_DEVICE_TOKEN",
       "platform_type": "pwa",
       "user_id": "user@example.com"
     }'
   ```

### SMS

1. Sign up for an SMS service provider (e.g., Twilio, Nexmo)
2. Get API credentials
3. Add the channel with config:
   ```json
   {
     "api_url": "https://api.sms-provider.com/send",
     "api_key": "YOUR_API_KEY"
   }
   ```

### Youdu (有度)

1. Get Youdu webhook URL from your admin
2. Add the channel with config:
   ```json
   {
     "webhook_url": "https://youdu.company.com/webhook",
     "app_id": "YOUR_APP_ID"
   }
   ```

## Troubleshooting

### Plugin Not Showing in UI

1. Check if the plugin is installed:
   ```bash
   pip list | grep airflow-notification-plugin
   ```

2. Verify plugin directory is in PYTHONPATH:
   ```bash
   python -c "import airflow_notification_plugin; print(airflow_notification_plugin.__file__)"
   ```

3. Check Airflow logs for errors:
   ```bash
   tail -f $AIRFLOW_HOME/logs/scheduler/latest/*.log
   ```

### Database Tables Not Created

1. Manually run the initialization:
   ```bash
   python -m airflow_notification_plugin.db_init
   ```

2. Check database connection:
   ```bash
   airflow db check
   ```

### Notifications Not Sending

1. Check the Airflow scheduler logs for errors
2. Verify channel configuration is correct
3. Ensure subscriptions are active
4. Test the webhook/API endpoint manually
5. Check rate limiting settings

## Upgrading

To upgrade to a newer version:

```bash
pip install --upgrade airflow-notification-plugin
```

Then restart Airflow services.

## Uninstallation

To remove the plugin:

```bash
pip uninstall airflow-notification-plugin
```

Note: This will not remove the database tables. To remove tables:

```python
from airflow_notification_plugin.models import Base
from airflow.settings import Session

session = Session()
engine = session.get_bind()
Base.metadata.drop_all(engine)
```

## Next Steps

- Customize notification templates
- Set up multiple channels for redundancy
- Configure rate limiting for high-volume DAGs
- Integrate with monitoring dashboards
- Set up device registration for mobile notifications
