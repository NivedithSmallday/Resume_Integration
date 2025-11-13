import pymysql
from contextlib import contextmanager
from typing import Dict, Any
import logging

# ------------------------------------------------------------------
# Logger Configuration
# ------------------------------------------------------------------

logger = logging.getLogger(__name__)
if not logger.handlers:
    # Prevent duplicate handlers if imported multiple times
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


# ------------------------------------------------------------------
# Custom Exception
# ------------------------------------------------------------------

class DatabaseConnectionError(Exception):
    """Custom exception for database connection issues."""
    pass


# ------------------------------------------------------------------
# Main Database Connection Class
# ------------------------------------------------------------------

class DatabaseConnection:
    """Handles MySQL database connections with proper resource management."""

    def __init__(self, config: Dict[str, Any]):
        self.host = config.get("host", "localhost")
        self.user = config.get("user", "root")
        self.password = config.get("password")
        self.database = config.get("database")
        self.charset = config.get("charset", "utf8mb4")
        self.port = int(config.get("port", 3306))

        # Validate configuration
        if not self.password:
            logger.error("❌ Database password not provided.")
            raise ValueError("Database password is required.")
        if not self.database:
            logger.error("❌ Database name not provided.")
            raise ValueError("Database name is required.")

        logger.info(f"🧩 DatabaseConnection initialized for DB: '{self.database}' on {self.host}:{self.port}")

    # ------------------------------------------------------------------
    # Create database if not exists
    # ------------------------------------------------------------------
    def create_database_if_not_exists(self) -> None:
        """Create database if it doesn't exist."""
        try:
            logger.info(f"🔍 Checking if database '{self.database}' exists...")
            temp_conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                charset=self.charset,
                port=self.port,
                cursorclass=pymysql.cursors.DictCursor,
            )

            with temp_conn.cursor() as cursor:
                cursor.execute(
                    f"CREATE DATABASE IF NOT EXISTS `{self.database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
                )
                temp_conn.commit()
                logger.info(f"✅ Database '{self.database}' verified or created successfully.")

        except pymysql.Error as e:
            logger.exception("❌ Failed to create or verify database.")
            raise DatabaseConnectionError(f"Failed to create database: {e}")

        finally:
            if "temp_conn" in locals():
                temp_conn.close()
                logger.debug("🔒 Temporary connection closed after DB creation check.")

    # ------------------------------------------------------------------
    # Connection context manager
    # ------------------------------------------------------------------
    @contextmanager
    def get_connection(self):
        """Context manager for safely opening and closing a database connection."""
        conn = None
        try:
            logger.debug(f"🔌 Establishing connection to database '{self.database}'...")
            conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset=self.charset,
                port=self.port,
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=False,
            )

            logger.debug(f"✅ Connected to '{self.database}' successfully.")
            yield conn

        except pymysql.Error as e:
            logger.exception("❌ Database connection or query failed.")
            if conn:
                conn.rollback()
                logger.warning("↩️ Transaction rolled back due to error.")
            raise DatabaseConnectionError(f"Database connection error: {e}")

        finally:
            if conn:
                conn.close()
                logger.debug(f"🔒 Connection to '{self.database}' closed.")
