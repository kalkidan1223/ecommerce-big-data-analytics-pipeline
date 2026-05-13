"""
Extract module for reading data from multiple sources.
Supports CSV, Parquet, and other formats.
"""

import logging
from typing import Dict
from pyspark.sql import SparkSession, DataFrame
from src.config import DATA_SOURCES, SPARK_CONFIG

logger = logging.getLogger(__name__)


class DataExtractor:
    """Extracts data from multiple sources using PySpark."""

    def __init__(self):
        """Initialize SparkSession with optimized configuration."""
        self.spark = self._create_spark_session()

    def _create_spark_session(self) -> SparkSession:
        """Create and configure SparkSession."""
        builder = SparkSession.builder
        for key, value in SPARK_CONFIG.items():
            builder = builder.config(key, value)
        
        spark = builder.getOrCreate()
        logger.info("SparkSession created successfully")
        return spark

    def extract_csv(self, source_name: str, **kwargs) -> DataFrame:
        """
        Extract data from CSV file.
        
        Args:
            source_name: Key from DATA_SOURCES
            **kwargs: Additional options for spark.read.csv()
        
        Returns:
            DataFrame with CSV data
        """
        file_path = DATA_SOURCES.get(source_name)
        if not file_path:
            raise ValueError(f"Unknown data source: {source_name}")
        
        logger.info(f"Extracting CSV from {file_path}")
        
        # Default CSV options
        options = {
            "header": True,
            "inferSchema": True,
            "multiLine": True,
            "escape": '"'
        }
        options.update(kwargs)
        
        df = self.spark.read.csv(file_path, **options)
        logger.info(f"Extracted {df.count()} rows from {source_name}")
        return df

    def extract_parquet(self, source_name: str) -> DataFrame:
        """
        Extract data from Parquet file.
        
        Args:
            source_name: Key from DATA_SOURCES
        
        Returns:
            DataFrame with Parquet data
        """
        file_path = DATA_SOURCES.get(source_name)
        if not file_path:
            raise ValueError(f"Unknown data source: {source_name}")
        
        logger.info(f"Extracting Parquet from {file_path}")
        
        df = self.spark.read.parquet(file_path)
        logger.info(f"Extracted {df.count()} rows from {source_name}")
        return df

    def extract_all(self) -> Dict[str, DataFrame]:
        """
        Extract data from all configured sources.
        
        Returns:
            Dictionary with source names as keys and DataFrames as values
        """
        data = {}
        
        # Extract CSV files
        data["orders"] = self.extract_csv("orders_csv")
        data["payments"] = self.extract_csv("payments_csv")
        
        # Extract Parquet file
        data["items"] = self.extract_parquet("items_parquet")
        
        logger.info("All data sources extracted successfully")
        return data

    def close(self):
        """Close SparkSession."""
        self.spark.stop()
        logger.info("SparkSession closed")
