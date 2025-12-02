
Airflow 通知管理插件 (后端服务)

该插件旨在提供一个可扩展、平台无关的通知中心，用于全局监控 Airflow 任务状态并分发告警。

1. 核心架构设计

-   **解耦设计**: 将事件监听、订阅管理和通知分发解耦，确保高可扩展性。
-   **平台无关性**: 通过通用的设备注册模型和策略模式（Strategy Pattern）支持多种客户端平台（PWA、iOS、Android 等）和多种通知渠道（Slack、短信、FCM 等）。

2. 功能需求

2.1. 管理界面 (基于 Flask-Admin)

-   **通知中心 UI**: 在 Airflow Web UI 导航栏中添加一个名为“通知中心”或“Notification Hub”的入口。
-   **渠道管理 UI**: 提供管理所有通知渠道配置的 CRUD 界面。
-   **订阅管理 UI**: 提供列表和表单，用于管理用户、DAG、事件类型和目标渠道之间的关联关系。
-   **模板管理 UI**: 管理和编辑通知消息模板（Jinja2）。
-   **设备注册管理 UI**: （管理员视角）查看和管理所有已注册的客户端设备令牌。

2.2. 数据库模型与存储

-   **`NotificationChannel`**: 存储渠道配置（如 Slack Webhook URL、FCM Server Key、SMS API Key 等）。
-   **`DagSubscription`**: 存储 DAG 订阅配置（`user_id`,  `dag_id`,  `event_type`,  `channel_id`）。
-   **`NotificationTemplate`**: 存储可配置的 Jinja2 消息模板。
-   **`DeviceRegistration`**: 存储客户端设备令牌 (`device_token`,  `platform_type`  [PWA, iOS, Android],  `user_id`)。

2.3. 事件监听与触发

-   **全局监听器**: 使用 Airflow 的  `listeners`  钩子（例如  `on_task_instance_failed`,  `on_task_instance_success`,  `on_sla_miss`）全局捕获所有 DAG 的任务状态变化。
-   **事件捕获**: 当事件发生时，捕获任务和 DAG 的所有相关元数据。

2.4. 通知分发中心 (Dispatcher Hub)

-   **订阅查询**: 根据捕获的事件，查询  `DagSubscription`  表以确定需要通知哪些用户和渠道。
-   **动态分发**: 根据渠道类型和平台类型，动态选择合适的分发策略。
-   **支持渠道列表**:
    -   **Slack Webhook**
    -   **SMS/电话 API**
    -   **有度 (Youdu) Webhook**
    -   **Firebase Cloud Messaging (FCM)**：支持 PWA 和 Android 推送。
    -   **APNS (Apple Push Notification Service)**：预留扩展支持原生 iOS 推送。
-   **模板渲染**: 使用 Jinja2 将事件数据填充到预定义的模板中。
-   **健壮性**: 实现重试机制、错误日志记录和抑制机制，防止通知风暴。

2.5. 客户端注册 API 接口

-   提供一个统一的 REST API 端点 (`POST /register-device`)，供所有客户端（PWA、iOS、Android）注册或更新其  `device_token`  和  `platform_type`。
