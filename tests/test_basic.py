"""
Simple tests to verify basic imports and syntax without requiring Airflow installation.
Run with: pytest tests/test_basic.py -v

Note: For these tests to work, install the package first:
    pip install -e .
"""

import os


def test_model_enums():
    """Test that model enums can be imported and have expected values."""
    from airflow_notification_plugin.models import EventType, ChannelType, PlatformType
    
    # Test EventType
    assert hasattr(EventType, 'TASK_SUCCESS')
    assert hasattr(EventType, 'TASK_FAILED')
    assert hasattr(EventType, 'TASK_RETRY')
    assert hasattr(EventType, 'SLA_MISS')
    assert hasattr(EventType, 'DAG_SUCCESS')
    assert hasattr(EventType, 'DAG_FAILED')
    
    # Test ChannelType
    assert hasattr(ChannelType, 'SLACK')
    assert hasattr(ChannelType, 'SMS')
    assert hasattr(ChannelType, 'YOUDU')
    assert hasattr(ChannelType, 'FCM')
    assert hasattr(ChannelType, 'APNS')
    
    # Test PlatformType
    assert hasattr(PlatformType, 'PWA')
    assert hasattr(PlatformType, 'IOS')
    assert hasattr(PlatformType, 'ANDROID')


def test_config_import():
    """Test that configuration can be imported."""
    from airflow_notification_plugin.config import config, NotificationConfig
    
    # Test configuration values
    assert hasattr(config, 'MAX_RETRY_ATTEMPTS')
    assert hasattr(config, 'ENABLE_SLACK')
    assert hasattr(config, 'RATE_LIMIT_ENABLED')
    
    # Test methods
    assert callable(config.is_channel_enabled)
    assert callable(config.get)


def test_project_structure():
    """Test that all required files exist."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    required_files = [
        'setup.py',
        'requirements.txt',
        'README.md',
        'INSTALLATION.md',
        'airflow_notification_plugin/__init__.py',
        'airflow_notification_plugin/models/__init__.py',
        'airflow_notification_plugin/views/__init__.py',
        'airflow_notification_plugin/api/__init__.py',
        'airflow_notification_plugin/dispatchers/__init__.py',
        'airflow_notification_plugin/listeners/__init__.py',
        'airflow_notification_plugin/config/__init__.py',
    ]
    
    for file in required_files:
        filepath = os.path.join(base_dir, file)
        assert os.path.exists(filepath), f"{file} not found"


def test_python_files_syntax():
    """Test that all Python files have valid syntax."""
    import py_compile
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    plugin_dir = os.path.join(base_dir, 'airflow_notification_plugin')
    
    for root, dirs, files in os.walk(plugin_dir):
        # Skip __pycache__ directories
        dirs[:] = [d for d in dirs if d != '__pycache__']
        
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                # This will raise SyntaxError if there's a problem
                py_compile.compile(filepath, doraise=True)
