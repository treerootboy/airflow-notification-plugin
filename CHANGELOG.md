# Changelog

All notable changes to the Airflow Notification Plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-12-02

### Added
- Initial release of Airflow Notification Plugin
- Multi-channel notification support:
  - Slack webhook integration
  - SMS notifications via API
  - Youdu (有度) webhook support
  - Firebase Cloud Messaging (FCM) for PWA and Android
  - Apple Push Notification Service (APNS) placeholder
- Flask-Admin management interface with views for:
  - Notification Channels configuration
  - DAG Subscriptions management
  - Notification Templates (Jinja2)
  - Device Registrations
- Event listeners for Airflow:
  - Task success/failure/retry events
  - DAG success/failure events
  - SLA miss events (placeholder)
- REST API endpoints:
  - POST /api/v1/notification/register-device
  - POST /api/v1/notification/unregister-device
- Database models:
  - NotificationChannel
  - DagSubscription
  - NotificationTemplate
  - DeviceRegistration
- Configuration management via environment variables
- Rate limiting support
- Retry mechanism with configurable settings
- Strategy pattern for notification dispatchers
- Jinja2 template rendering for notifications
- Default notification templates
- Comprehensive documentation:
  - README.md with usage examples
  - INSTALLATION.md with setup guide
  - CONTRIBUTING.md for developers
  - Example scripts and test DAG
- Project structure with proper Python packaging
- setup.py for pip installation
- requirements.txt for dependencies

### Security
- Input validation for API endpoints
- JSON config validation for channels
- Active/inactive status for channels and subscriptions
- Device token management with user association

[0.1.0]: https://github.com/treerootboy/airflow-notification-plugin/releases/tag/v0.1.0
