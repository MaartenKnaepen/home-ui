import os
from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings
import yaml


class Service(BaseModel):
    """Model for a service entry in the dashboard."""
    name: str
    url: str
    icon: str
    description: str | None = None


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    dashboard_password: str = "changeme"
    secret_key: str = "change-this-to-a-random-string"
    config_path: str = "services.yaml"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def load_services(config_path: str = "services.yaml") -> list[Service]:
    """Load services from YAML configuration file."""
    try:
        config_file = Path(config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_file, "r") as f:
            data = yaml.safe_load(f)
        
        services_data = data.get("services", [])
        return [Service(**service) for service in services_data]
    except Exception as e:
        print(f"Error loading services: {e}")
        return []
