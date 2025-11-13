import pymysql
from contextlib import contextmanager
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class DatabaseConnectionError(Exception):
    """Custom exception for database connection issues"""
    pass


class DatabaseConnection:
    """Handles MySQL database connections with proper resource management"""

    def __init__(self, config: Dict[str, Any]):
        self.host = config.get('host', 'localhost')
        self.user = config.get('user', 'root')
        self.password = config.get('password')
        self.database = config.get('database')
        self.charset = config.get('charset', 'utf8mb4')

        if not self.password:
            raise ValueError("Database password is required")
        if not self.database:
            raise ValueError("Database name is required")

    def create_database_if_not_exists(self) -> None:
        """Create database if it doesn't exist"""
        try:
            temp_conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                charset=self.charset,
                cursorclass=pymysql.cursors.DictCursor
            )

            with temp_conn.cursor() as cursor:
                cursor.execute(
                    f"CREATE DATABASE IF NOT EXISTS `{self.database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                temp_conn.commit()

        except pymysql.Error as e:
            logger.error(f"Failed to create database: {e}")
            raise DatabaseConnectionError(f"Failed to create database: {e}")
        finally:
            if 'temp_conn' in locals():
                temp_conn.close()

    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = None
        try:
            conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset=self.charset,
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=False
            )
            yield conn
        except pymysql.Error as e:
            logger.error(f"Database connection error: {e}")
            if conn:
                conn.rollback()
            raise DatabaseConnectionError(f"Database connection error: {e}")
        finally:
            if conn:
                conn.close()