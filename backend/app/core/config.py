"""
Application configuration management.
Loads settings from config files and environment variables.
"""
import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field
import yaml

# Project root (backend directory)
PROJECT_ROOT = Path(__file__).parent.parent.parent
CONFIG_DIR = PROJECT_ROOT.parent / "config"


class Settings(BaseSettings):
    """Application settings."""
    
    # Server
    host: str = Field(default="localhost", description="API host")
    port: int = Field(default=8000, description="API port")
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        description="Allowed CORS origins"
    )
    
    # Storage paths
    db_path: str = Field(
        default="data/db/cortexdesk.db",
        description="SQLite database path"
    )
    vector_db_path: str = Field(
        default="data/embeddings",
        description="Chroma vector DB path"
    )
    vault_path: str = Field(
        default="data/vault",
        description="Encrypted file vault path"
    )
    logs_path: str = Field(
        default="data/logs",
        description="Logs directory path"
    )
    
    # Security
    encryption_enabled: bool = Field(default=True, description="Enable encryption")
    require_permissions: bool = Field(default=True, description="Require explicit permissions")
    external_network_enabled: bool = Field(
        default=False,
        description="Allow external network calls (must be False)"
    )
    
    # Feature flags
    live_meeting_mode: bool = Field(default=True, description="Enable live meeting mode")
    research_workspace: bool = Field(default=True, description="Enable research workspace")
    task_extraction: bool = Field(default=True, description="Enable task extraction")
    scheduler: bool = Field(default=True, description="Enable scheduler")
    knowledge_graph: bool = Field(default=True, description="Enable knowledge graph")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


def load_yaml_config(file_path: Path) -> dict:
    """Load YAML configuration file."""
    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    return {}


def get_settings() -> Settings:
    """Get application settings, loading from YAML config if available."""
    # Load app.yaml
    app_config = load_yaml_config(CONFIG_DIR / "app.yaml")
    
    # Override defaults with YAML values
    settings_dict = {}
    
    if "backend" in app_config:
        backend_config = app_config["backend"]
        settings_dict["host"] = backend_config.get("host", "localhost")
        settings_dict["port"] = backend_config.get("port", 8000)
        settings_dict["cors_origins"] = backend_config.get("cors_origins", ["http://localhost:5173"])
    
    if "storage" in app_config:
        storage_config = app_config["storage"]
        settings_dict["db_path"] = storage_config.get("db_path", "data/db/cortexdesk.db")
        settings_dict["vector_db_path"] = storage_config.get("vector_db_path", "data/embeddings")
        settings_dict["vault_path"] = storage_config.get("vault_path", "data/vault")
        settings_dict["logs_path"] = storage_config.get("logs_path", "data/logs")
    
    if "security" in app_config:
        security_config = app_config["security"]
        settings_dict["encryption_enabled"] = security_config.get("encryption_enabled", True)
        settings_dict["require_permissions"] = security_config.get("require_permissions", True)
        settings_dict["external_network_enabled"] = security_config.get("external_network_enabled", False)
    
    if "features" in app_config:
        features_config = app_config["features"]
        settings_dict["live_meeting_mode"] = features_config.get("live_meeting_mode", True)
        settings_dict["research_workspace"] = features_config.get("research_workspace", True)
        settings_dict["task_extraction"] = features_config.get("task_extraction", True)
        settings_dict["scheduler"] = features_config.get("scheduler", True)
        settings_dict["knowledge_graph"] = features_config.get("knowledge_graph", True)
    
    # Create Settings instance, allowing environment variables to override
    return Settings(**settings_dict)


# Global settings instance
settings = get_settings()

