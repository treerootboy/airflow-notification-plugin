"""
Simple tests to verify basic imports and syntax without requiring Airflow installation.
"""

def test_imports():
    """Test that basic modules can be imported."""
    try:
        # Test models can be imported (without initializing)
        import sys
        import os
        
        # Add parent directory to path
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Test individual module imports without Airflow dependencies
        print("Testing model imports...")
        from airflow_notification_plugin.models import (
            EventType, ChannelType, PlatformType
        )
        print("✓ Models enums imported successfully")
        
        print("\nTesting config imports...")
        from airflow_notification_plugin.config import NotificationConfig
        print("✓ Config imported successfully")
        
        print("\nAll imports successful!")
        return True
        
    except Exception as e:
        print(f"✗ Import error: {str(e)}")
        return False


def test_enums():
    """Test that enums are defined correctly."""
    try:
        from airflow_notification_plugin.models import EventType, ChannelType, PlatformType
        
        print("\nTesting enums...")
        
        # Test EventType
        assert hasattr(EventType, 'TASK_SUCCESS')
        assert hasattr(EventType, 'TASK_FAILED')
        assert hasattr(EventType, 'TASK_RETRY')
        print("✓ EventType enum has all expected values")
        
        # Test ChannelType
        assert hasattr(ChannelType, 'SLACK')
        assert hasattr(ChannelType, 'SMS')
        assert hasattr(ChannelType, 'YOUDU')
        assert hasattr(ChannelType, 'FCM')
        assert hasattr(ChannelType, 'APNS')
        print("✓ ChannelType enum has all expected values")
        
        # Test PlatformType
        assert hasattr(PlatformType, 'PWA')
        assert hasattr(PlatformType, 'IOS')
        assert hasattr(PlatformType, 'ANDROID')
        print("✓ PlatformType enum has all expected values")
        
        return True
        
    except Exception as e:
        print(f"✗ Enum test error: {str(e)}")
        return False


def test_config():
    """Test configuration."""
    try:
        from airflow_notification_plugin.config import config
        
        print("\nTesting configuration...")
        
        # Test configuration values
        assert hasattr(config, 'MAX_RETRY_ATTEMPTS')
        assert hasattr(config, 'ENABLE_SLACK')
        print("✓ Config has expected attributes")
        
        # Test channel enabled check
        assert callable(config.is_channel_enabled)
        print("✓ Config methods are callable")
        
        return True
        
    except Exception as e:
        print(f"✗ Config test error: {str(e)}")
        return False


def test_structure():
    """Test project structure."""
    import os
    
    print("\nTesting project structure...")
    
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
    
    all_exist = True
    for file in required_files:
        filepath = os.path.join(base_dir, file)
        if os.path.exists(filepath):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - NOT FOUND")
            all_exist = False
    
    return all_exist


if __name__ == "__main__":
    print("="*60)
    print("Running Basic Tests")
    print("="*60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Enums", test_enums()))
    results.append(("Config", test_config()))
    results.append(("Structure", test_structure()))
    
    print("\n" + "="*60)
    print("Test Results Summary")
    print("="*60)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
    print("="*60)
    
    exit(0 if all_passed else 1)
