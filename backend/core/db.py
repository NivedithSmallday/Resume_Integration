import os
import logging
from typing import Dict, Any
from dotenv import load_dotenv

from database.connection import DatabaseConnection
from database.schema_manager import SchemaManager
from repositories.resume_repository import ResumeRepository
from services.resume_service import ResumeService
from core.schema import DB_SCHEMA  # ensure this exposes DB_SCHEMA

logger = logging.getLogger(__name__)


class ResumeDB:
    """Database orchestrator for resumes."""

    def __init__(self, config: Dict[str, Any] = None):
        # --- Load environment variables ---
        load_dotenv()

        # --- Read configuration ---
        env_config = {
            "host": os.getenv("DB_HOST", "localhost"),
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASSWORD", ""),
            "database": os.getenv("DB_NAME", "resume_parser"),
            "port": int(os.getenv("DB_PORT", "3306")),
        }

        # Allow overriding through constructor (useful for testing)
        self.config = config or env_config

        # Validate essential keys
        self._validate_config(self.config)

        # --- Initialize database ---
        try:
            # 1️⃣ Connect
            self.db_connection = DatabaseConnection(self.config)
            logger.info("✅ Database connection initialized")

            # 2️⃣ Ensure database exists
            self.db_connection.create_database_if_not_exists()
            logger.info(f"✅ Database '{self.config['database']}' verified/created")

            # 3️⃣ Apply schema
            self.schema_manager = SchemaManager(self.db_connection, DB_SCHEMA)
            self.schema_manager.create_schema()
            logger.info("✅ Schema applied successfully")

            # 4️⃣ Initialize repository and service
            self.resume_repository = ResumeRepository(self.db_connection)
            self.resume_service = ResumeService(self.resume_repository)

            logger.info("🎯 ResumeDB initialized successfully")

        except Exception as e:
            logger.error(f"❌ Failed to initialize ResumeDB: {e}")
            raise

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------

    def _validate_config(self, config: Dict[str, Any]):
        """Ensure required DB configuration values are present."""
        required = ["host", "user", "database"]
        missing = [key for key in required if not config.get(key)]
        if missing:
            raise ValueError(f"❌ Missing required DB config keys: {', '.join(missing)}")

    # ------------------------------------------------------------------
    # Convenience methods (optional passthrough)
    # ------------------------------------------------------------------

    def insert_resume(self, data: Dict[str, Any]) -> int:
        """Insert resume and return ID."""
        return self.resume_service.create_resume(data)

    def resume_exists(self, email: str = None, phone: str = None) -> bool:
        """Check if a resume exists by email or phone."""
        return self.resume_repository.exists_by_email_or_phone(email, phone)
