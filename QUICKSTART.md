# Quick Start Guide

Get started with the Airflow Notification Plugin in 5 minutes!

## Prerequisites

- Apache Airflow 2.0+ installed
- Python 3.7+
- One notification service account (e.g., Slack webhook)

## Installation

```bash
# Clone the repository
git clone https://github.com/treerootboy/airflow-notification-plugin.git
cd airflow-notification-plugin

# Install the plugin
pip install -e .
```

## Setup

### 1. Initialize Database (1 minute)

```bash
python -m airflow_notification_plugin.db_init
```

### 2. Restart Airflow (1 minute)

```bash
# Stop and restart Airflow services
airflow webserver stop && airflow scheduler stop
airflow webserver -D && airflow scheduler -D
```

### 3. Configure a Channel (2 minutes)

1. Open Airflow Web UI (http://localhost:8080)
2. Navigate to **Notification Hub** → **Notification Channels**
3. Click **Create**
4. Fill in:
   - **Name**: `my-slack-channel`
   - **Channel Type**: `slack`
   - **Config**:
     ```json
     {"webhook_url": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"}
     ```
   - Check **Is Active**
5. Click **Save**

### 4. Create a Subscription (1 minute)

1. Go to **Notification Hub** → **DAG Subscriptions**
2. Click **Create**
3. Fill in:
   - **User ID**: `your-email@example.com`
   - **DAG ID**: `*` (for all DAGs) or specific DAG name
   - **Event Type**: `task_failed`
   - **Channel ID**: Select your channel
   - Check **Is Active**
4. Click **Save**

## Test It!

Run the example DAG:

```bash
# Copy example DAG to your DAGs folder
cp examples/notification_test_dag.py $AIRFLOW_HOME/dags/

# Trigger the DAG
airflow dags trigger notification_test_dag
```

You should receive a Slack notification when the DAG completes!

## What's Next?

- **Customize Templates**: Create custom notification templates with Jinja2
- **Add More Channels**: Set up SMS, FCM, or Youdu
- **Mobile Push**: Register devices for mobile notifications
- **Monitor Multiple DAGs**: Create subscriptions for different DAGs and events

## Common Issues

### Plugin Not Showing in UI

1. Check installation: `pip list | grep airflow-notification-plugin`
2. Restart Airflow: `airflow webserver stop && airflow webserver -D`
3. Check logs: `tail -f $AIRFLOW_HOME/logs/scheduler/latest/*.log`

### Notifications Not Sending

1. Verify channel config is correct (test webhook manually)
2. Check subscription is active
3. Check Airflow scheduler logs for errors
4. Verify event type matches (e.g., `task_failed` vs `task_success`)

## Full Documentation

- [Installation Guide](INSTALLATION.md)
- [Full README](README.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Feature List (Chinese)](FEATURES_CN.md)

## Get Help

- [GitHub Issues](https://github.com/treerootboy/airflow-notification-plugin/issues)
- Check documentation
- Review example scripts in `examples/`

Happy notifying! 🎉
