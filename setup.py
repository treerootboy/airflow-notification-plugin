"""Setup configuration for the Airflow Notification Plugin."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="airflow-notification-plugin",
    version="0.1.0",
    author="TreeRootBoy",
    description="A comprehensive notification management plugin for Apache Airflow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/treerootboy/airflow-notification-plugin",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "apache-airflow>=2.0.0",
        "flask>=1.1.0",
        "flask-admin>=1.5.0",
        "sqlalchemy>=1.3.0",
        "requests>=2.25.0",
        "jinja2>=2.11.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "black>=21.0",
            "flake8>=3.8.0",
        ],
    },
    entry_points={
        "airflow.plugins": [
            "notification_hub = airflow_notification_plugin:AirflowNotificationPlugin",
        ],
    },
    include_package_data=True,
    package_data={
        "airflow_notification_plugin": ["templates/*"],
    },
)
