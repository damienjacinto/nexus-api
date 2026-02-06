"""Configuration management for Nexus client."""

import os
from typing import Optional
from dotenv import load_dotenv


class Config:
    """Configuration loader for Nexus client."""

    def __init__(self, env_file: Optional[str] = None):
        """
        Load configuration from environment or .env file.

        Args:
            env_file: Path to .env file (optional)
        """
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()

        self.nexus_url = os.getenv('NEXUS_URL', 'http://localhost:8081')
        self.nexus_username = os.getenv('NEXUS_USERNAME')
        self.nexus_password = os.getenv('NEXUS_PASSWORD')
        self.verify_ssl = os.getenv('NEXUS_VERIFY_SSL', 'true').lower() == 'true'
        self.timeout = int(os.getenv('NEXUS_TIMEOUT', '30'))

    def get_client_kwargs(self) -> dict:
        """
        Get kwargs for NexusClient initialization.

        Returns:
            Dict of kwargs for NexusClient
        """
        return {
            'base_url': self.nexus_url,
            'username': self.nexus_username,
            'password': self.nexus_password,
            'verify_ssl': self.verify_ssl,
            'timeout': self.timeout
        }
