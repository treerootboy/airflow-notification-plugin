# Contributing to Airflow Notification Plugin

Thank you for your interest in contributing to the Airflow Notification Plugin! This document provides guidelines and instructions for contributing.

## Development Setup

### Prerequisites

- Python 3.7 or higher
- Apache Airflow 2.0.0 or higher
- Git

### Setting Up Development Environment

1. **Fork and clone the repository:**

```bash
git clone https://github.com/YOUR_USERNAME/airflow-notification-plugin.git
cd airflow-notification-plugin
```

2. **Create a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -e ".[dev]"
```

4. **Install Airflow (if not already installed):**

```bash
pip install apache-airflow
```

## Code Style

We follow PEP 8 guidelines with some modifications:

- Line length: 100 characters
- Use double quotes for strings
- Use type hints where appropriate

### Formatting Tools

Run these before committing:

```bash
# Format code
black airflow_notification_plugin/

# Check style
flake8 airflow_notification_plugin/
```

## Project Structure

```
airflow-notification-plugin/
├── airflow_notification_plugin/
│   ├── __init__.py              # Plugin entry point
│   ├── models/                   # Database models
│   │   └── __init__.py
│   ├── views/                    # Flask-Admin views
│   │   └── __init__.py
│   ├── api/                      # REST API endpoints
│   │   ├── __init__.py
│   │   └── device_registration.py
│   ├── dispatchers/              # Notification dispatchers
│   │   ├── __init__.py
│   │   ├── dispatcher.py
│   │   └── handlers.py
│   ├── listeners/                # Airflow event listeners
│   │   └── __init__.py
│   └── config/                   # Configuration
│       └── __init__.py
├── examples/                     # Example scripts
├── tests/                        # Tests
├── setup.py                      # Package setup
└── requirements.txt              # Dependencies
```

## Making Changes

### Workflow

1. **Create a new branch:**

```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes**

3. **Test your changes:**

```bash
python -m pytest tests/
```

4. **Commit your changes:**

```bash
git add .
git commit -m "Description of your changes"
```

5. **Push to your fork:**

```bash
git push origin feature/your-feature-name
```

6. **Create a Pull Request**

### Commit Messages

Follow the conventional commits format:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

Example:
```
feat: add support for Microsoft Teams notifications
```

## Adding New Features

### Adding a New Notification Channel

1. **Create the handler in `dispatchers/handlers.py`:**

```python
class TeamsHandler(NotificationHandler):
    """Handler for Microsoft Teams notifications."""
    
    def send(self, config: Dict[str, Any], message: str, **kwargs) -> bool:
        # Implementation
        pass
```

2. **Register the handler:**

```python
HANDLERS = {
    # ... existing handlers
    "teams": TeamsHandler(),
}
```

3. **Add the channel type to `models/__init__.py`:**

```python
class ChannelType(enum.Enum):
    # ... existing types
    TEAMS = "teams"
```

4. **Update documentation**

5. **Add tests**

### Adding New Event Types

1. **Add to `EventType` enum in `models/__init__.py`:**

```python
class EventType(enum.Enum):
    # ... existing types
    YOUR_NEW_EVENT = "your_new_event"
```

2. **Add listener in `listeners/__init__.py`:**

```python
@hookimpl
def on_your_new_event(context):
    event_data = _extract_event_data(context)
    dispatcher.dispatch(EventType.YOUR_NEW_EVENT, event_data)
```

3. **Add default template in `dispatchers/dispatcher.py`**

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=airflow_notification_plugin tests/

# Run specific test file
python -m pytest tests/test_basic.py
```

### Writing Tests

Place tests in the `tests/` directory:

```python
def test_your_feature():
    """Test description."""
    # Test implementation
    assert True
```

## Documentation

### Updating Documentation

- **README.md**: Update for user-facing changes
- **INSTALLATION.md**: Update for installation changes
- **Code comments**: Add docstrings to all functions and classes
- **Examples**: Add examples for new features

### Documentation Style

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """Brief description.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When something goes wrong
    """
```

## Pull Request Process

1. **Update documentation** for any user-facing changes
2. **Add tests** for new features
3. **Ensure all tests pass**
4. **Update CHANGELOG** (if exists)
5. **Request review** from maintainers

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe how you tested your changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
```

## Code Review

All submissions require review. We use GitHub pull requests for this purpose.

### Review Criteria

- Code quality and style
- Test coverage
- Documentation completeness
- Backward compatibility
- Performance considerations

## Reporting Issues

### Bug Reports

Use the issue tracker and include:

- Description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment (Python version, Airflow version, etc.)
- Logs or error messages

### Feature Requests

Include:

- Clear description of the feature
- Use case and motivation
- Proposed implementation (optional)
- Alternatives considered (optional)

## Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Documentation**: Check README.md and INSTALLATION.md first

## Code of Conduct

Be respectful and inclusive. We aim to create a welcoming environment for all contributors.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- GitHub contributors list
- Release notes (for significant contributions)
- CONTRIBUTORS.md file (if created)

Thank you for contributing! 🎉
