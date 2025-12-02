# Airflow Notification Plugin

A comprehensive, extensible notification management system for Apache Airflow that provides multi-channel notification support with a centralized management interface.

## Features

- 🔔 **Multi-Channel Support**: Slack, SMS, Youdu (有度), Firebase Cloud Messaging (FCM), Apple Push Notification Service (APNS)
- 🎯 **Event-Driven**: Global listeners for task success, failure, retry, SLA miss, and DAG completion
- 🎨 **Template Management**: Customizable Jinja2 templates for notification messages
- 📱 **Device Registration**: REST API for PWA, iOS, and Android client registration
- 🛠️ **Admin UI**: Flask-Admin based management interface integrated into Airflow Web UI
- 🔌 **Plugin Architecture**: Easy integration with existing Airflow installations
- 📊 **Subscription Management**: Fine-grained control over who receives what notifications

## Architecture

The plugin uses a decoupled architecture with the following components:

1. **Event Listeners**: Capture Airflow task and DAG events globally
2. **Subscription Manager**: Store and query user notification preferences
3. **Dispatcher Hub**: Route notifications to appropriate channels using strategy pattern
4. **Channel Handlers**: Implement channel-specific logic for each notification type
5. **Template Engine**: Render customizable message templates with Jinja2

## Installation

### From Source

```bash
git clone https://github.com/treerootboy/airflow-notification-plugin.git
cd airflow-notification-plugin
pip install -e .
```

### Using pip

```bash
pip install airflow-notification-plugin
```

## Quick Start

### 1. Initialize Database

After installation, initialize the plugin tables:

```python
from airflow_notification_plugin.db_init import init_db, create_default_templates

init_db()
create_default_templates()
```

Or run the initialization script:

```bash
python -m airflow_notification_plugin.db_init
```

### 2. Configure Channels

Access the Airflow Web UI and navigate to **Notification Hub** → **Notification Channels** to add your notification channels.

#### Example: Slack Channel

- **Name**: `production-alerts`
- **Channel Type**: `slack`
- **Config**: `{"webhook_url": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"}`

#### Example: FCM Channel

- **Name**: `mobile-push`
- **Channel Type**: `fcm`
- **Config**: `{"server_key": "YOUR_FCM_SERVER_KEY"}`

### 3. Create Subscriptions

Go to **Notification Hub** → **DAG Subscriptions** to create notification subscriptions:

- **User ID**: `user@example.com`
- **DAG ID**: `my_important_dag`
- **Event Type**: `task_failed`
- **Channel**: Select from your configured channels

### 4. Register Devices (Optional)

For mobile/PWA push notifications, register devices via the REST API:

```bash
curl -X POST http://your-airflow-host/api/v1/notification/register-device \
  -H "Content-Type: application/json" \
  -d '{
    "device_token": "YOUR_DEVICE_TOKEN",
    "platform_type": "pwa",
    "user_id": "user@example.com"
  }'
```

## Configuration

Set environment variables to customize plugin behavior:

```bash
# Database (uses Airflow's database by default)
export AIRFLOW_NOTIFICATION_DB_URL="postgresql://user:pass@localhost/airflow"

# Retry settings
export NOTIFICATION_MAX_RETRIES=3
export NOTIFICATION_RETRY_DELAY=5

# Rate limiting
export NOTIFICATION_RATE_LIMIT_ENABLED=true
export NOTIFICATION_RATE_LIMIT_PER_MIN=60

# Feature flags
export NOTIFICATION_ENABLE_SLACK=true
export NOTIFICATION_ENABLE_SMS=true
export NOTIFICATION_ENABLE_YOUDU=true
export NOTIFICATION_ENABLE_FCM=true
export NOTIFICATION_ENABLE_APNS=false
```

## Channel Configuration Examples

### Slack

```json
{
  "webhook_url": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
  "username": "Airflow Bot",
  "icon_emoji": ":airflow:"
}
```

### SMS

```json
{
  "api_url": "https://api.sms-provider.com/send",
  "api_key": "YOUR_API_KEY"
}
```

### Youdu (有度)

```json
{
  "webhook_url": "https://youdu.company.com/webhook",
  "app_id": "YOUR_APP_ID"
}
```

### Firebase Cloud Messaging

```json
{
  "server_key": "YOUR_FCM_SERVER_KEY"
}
```

## Template Variables

Available variables in notification templates:

### Task Events
- `dag_id`: DAG identifier
- `task_id`: Task identifier
- `execution_date`: Task execution date
- `state`: Task state
- `try_number`: Current try number
- `max_tries`: Maximum retries
- `duration`: Task duration in seconds
- `start_date`: Task start date
- `end_date`: Task end date
- `hostname`: Execution hostname

### DAG Events
- `dag_id`: DAG identifier
- `run_id`: DAG run identifier
- `execution_date`: DAG execution date
- `state`: DAG state
- `start_date`: DAG start date
- `end_date`: DAG end date
- `external_trigger`: Whether externally triggered

## API Reference

### POST /api/v1/notification/register-device

Register or update a device for push notifications.

**Request:**
```json
{
  "device_token": "string",
  "platform_type": "pwa|ios|android",
  "user_id": "string"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Device registered successfully",
  "device_id": 123
}
```

### POST /api/v1/notification/unregister-device

Unregister a device.

**Request:**
```json
{
  "device_token": "string"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Device unregistered successfully"
}
```

## Event Listeners

The plugin automatically registers listeners for the following Airflow events:

- `on_task_instance_success`: Task completed successfully
- `on_task_instance_failed`: Task failed
- `on_task_instance_running`: Task started (used for retry detection)
- `on_dag_run_success`: DAG run completed successfully
- `on_dag_run_failed`: DAG run failed

## Database Models

### NotificationChannel
Stores notification channel configurations (Slack webhooks, API keys, etc.)

### DagSubscription
Links users, DAGs, events, and notification channels

### NotificationTemplate
Customizable Jinja2 message templates for different event and channel types

### DeviceRegistration
Stores device tokens for mobile/PWA push notifications

## Development

### Running Tests

```bash
pip install -e ".[dev]"
pytest
```

### Code Formatting

```bash
black airflow_notification_plugin/
flake8 airflow_notification_plugin/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues and questions, please open an issue on [GitHub](https://github.com/treerootboy/airflow-notification-plugin/issues).