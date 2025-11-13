from typing import List
import logging

from database.connection import DatabaseConnection

logger = logging.getLogger(__name__)


class SchemaManager:
    """Handles database schema creation and management"""

    def __init__(self, db_connection: DatabaseConnection, schema: str):
        self.db_connection = db_connection
        self.schema = schema

    def create_schema(self) -> None:
        """Create database schema if it doesn't exist"""
        try:
            with self.db_connection.get_connection() as conn:
                with conn.cursor() as cursor:
                    statements = self._parse_schema_statements()
                    for statement in statements:
                        cursor.execute(statement)
                    conn.commit()
                    logger.info("Database schema created successfully")
        except Exception as e:
            logger.error(f"Failed to create schema: {e}")
            raise

    def _parse_schema_statements(self) -> List[str]:
        """Parse schema string into individual SQL statements"""
        statements = []
        for stmt in self.schema.split(";"):
            stmt = stmt.strip()
            if stmt:
                statements.append(stmt)
        return statements