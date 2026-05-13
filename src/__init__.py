"""
Data Pipeline Package
Comprehensive ETL solution with PySpark, DuckDB, and Airflow orchestration.
"""

__version__ = "1.0.0"
__author__ = "Data Engineering Team"

from src.config import (
    PROJECT_ROOT,
    DATA_DIR,
    DUCKDB_PATH,
    SPARK_CONFIG,
    DATA_SOURCES
)

__all__ = [
    "PROJECT_ROOT",
    "DATA_DIR",
    "DUCKDB_PATH",
    "SPARK_CONFIG",
    "DATA_SOURCES"
]
