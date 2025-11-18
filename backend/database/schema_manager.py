from typing import List
import logging

from database.connection import DatabaseConnection

# ------------------------------------------------------------------
# Logger Configuration
# ------------------------------------------------------------------
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


# ------------------------------------------------------------------
# Schema Manager
# ------------------------------------------------------------------
class SchemaManager:
    """Handles database schema creation and management."""

    def __init__(self, db_connection: DatabaseConnection, schema: str):
        self.db_connection = db_connection
        self.schema = schema
        logger.info("🧩 SchemaManager initialized successfully.")

    # ------------------------------------------------------------------
    # Create schema
    # ------------------------------------------------------------------
    def create_schema(self) -> None:
        """Create database schema if it doesn't exist."""
        try:
            logger.info("⚙️  Starting schema creation process...")
            statements = self._parse_schema_statements()
            logger.debug(f"Parsed {len(statements)} SQL statements from schema definition.")

            with self.db_connection.get_connection() as conn:
                with conn.cursor() as cursor:
                    for i, statement in enumerate(statements, start=1):
                        logger.debug(f"🧱 Executing statement {i}/{len(statements)}: {statement[:80]}...")
                        cursor.execute(statement)
                    conn.commit()

            logger.info("✅ Database schema created successfully.")

        except Exception as e:
            logger.exception("❌ Failed to create database schema.")
            raise

    # ------------------------------------------------------------------
    # Parse schema string into individual SQL statements
    # ------------------------------------------------------------------
    def _parse_schema_statements(self) -> List[str]:
        """Parse schema string into individual SQL statements."""
        try:
            if not self.schema:
                logger.warning("⚠️  No schema definition provided.")
                return []

            statements = []
            for stmt in self.schema.split(";"):
                stmt = stmt.strip()
                if stmt:
                    statements.append(stmt)

            logger.debug(f"Schema parsing complete — {len(statements)} valid SQL statements found.")
            return statements

        except Exception as e:
            logger.error(f"❌ Failed to parse schema: {e}")
            raise
