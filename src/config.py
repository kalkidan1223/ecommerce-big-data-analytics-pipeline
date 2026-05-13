"""
Configuration module for the data pipeline.
Handles all configuration parameters for PySpark, DuckDB, and Airflow.
"""

import os
from datetime import datetime
from pathlib import Path

# Base paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
LOGS_DIR = PROJECT_ROOT / "logs"
SQL_DIR = PROJECT_ROOT / "sql"

# Create directories if they don't exist
for dir_path in [PROCESSED_DATA_DIR, LOGS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Data sources
DATA_SOURCES = {
    "orders_csv": str(RAW_DATA_DIR / "olist_orders_dataset.csv"),
    "payments_csv": str(RAW_DATA_DIR / "olist_order_payments_dataset.csv"),
    "items_parquet": str(RAW_DATA_DIR / "olist_order_items_dataset.parquet"),
}

# DuckDB configuration
DUCKDB_PATH = str(PROCESSED_DATA_DIR / "analytics.duckdb")
DUCKDB_READONLY = False

# PySpark configuration
SPARK_CONFIG = {
    "spark.app.name": "DataPipeline",
    "spark.master": "local[*]",
    "spark.sql.shuffle.partitions": "8",
    "spark.sql.adaptive.enabled": "true",
    "spark.sql.adaptive.coalescePartitions.enabled": "true",
}

# Airflow configuration
AIRFLOW_DAG_ID = "data_pipeline_dag"
PIPELINE_SCHEDULE_INTERVAL = "0 2 * * *"  # Run daily at 2 AM
PIPELINE_START_DATE = datetime(2024, 1, 1)

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Performance tuning
BATCH_SIZE = 10000
PARTITION_SIZE_MB = 128
