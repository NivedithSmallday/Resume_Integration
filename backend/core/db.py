# core/db.py
import logging
from typing import Dict, Any

from database.connection import DatabaseConnection
from database.schema_manager import SchemaManager
from repositories.resume_repository import ResumeRepository
from services.resume_service import ResumeService
from core.schema import DB_SCHEMA  # make sure schema/__init__.py or schema/schema.py exposes DB_SCHEMA

logger = logging.getLogger(__name__)


class ResumeDB:
    """Database orchestrator for resumes"""

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = {
                "host": "localhost",
                "user": "root",
                "password": "Prajitharaghu1",  # ⚠️ replace with .env variable later
                "database": "resume_parser",
            }

        # 1. Create connection
        self.db_connection = DatabaseConnection(config)

        # 2. Ensure DB exists
        self.db_connection.create_database_if_not_exists()

        # 3. Apply schema
        self.schema_manager = SchemaManager(self.db_connection, DB_SCHEMA)
        self.schema_manager.create_schema()

        # 4. Build repository + service
        self.resume_repository = ResumeRepository(self.db_connection)
        self.resume_service = ResumeService(self.resume_repository)

        logger.info("✅ ResumeDB initialized successfully")

    # ---- Convenience methods (so you don’t always go into .resume_service) ----

    def insert_resume(self, data: Dict[str, Any]) -> int:
        """Insert resume and return ID"""
        return self.resume_service.create_resume(data)

    def resume_exists(self, email: str = None, phone: str = None) -> bool:
        """Check if resume exists by email/phone"""
        return self.resume_repository.exists_by_email_or_phone(email, phone)






