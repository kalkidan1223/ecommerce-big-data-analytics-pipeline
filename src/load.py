"""
Load module for writing transformed data to DuckDB.
Handles database operations and table management.
"""

import logging
from typing import Dict, List
import duckdb
from pyspark.sql import DataFrame
from src.config import DUCKDB_PATH

logger = logging.getLogger(__name__)


class DuckDBLoader:
    """Loads and manages data in DuckDB analytical database."""

    def __init__(self, db_path: str = DUCKDB_PATH):
        """
        Initialize DuckDB connection.
        
        Args:
            db_path: Path to DuckDB database file
        """
        self.db_path = db_path
        self.conn = None
        self._connect()

    def _connect(self):
        """Establish connection to DuckDB."""
        try:
            self.conn = duckdb.connect(self.db_path)
            logger.info(f"Connected to DuckDB at {self.db_path}")
        except Exception as e:
            logger.error(f"Failed to connect to DuckDB: {e}")
            raise

    def load_spark_df(
        self,
        spark_df: DataFrame,
        table_name: str,
        mode: str = "overwrite",
        create_indexes: bool = True
    ):
        """
        Load PySpark DataFrame into DuckDB table.
        
        Args:
            spark_df: PySpark DataFrame to load
            table_name: Target table name
            mode: 'overwrite' or 'append'
            create_indexes: Whether to create indexes on key columns
        """
        try:
            # Convert Spark DF to Arrow format (efficient format)
            logger.info(f"Loading data into table '{table_name}'")
            
            arrow_table = spark_df.toArrow()
            
            # Drop table if overwrite mode
            if mode == "overwrite":
                self.conn.execute(f"DROP TABLE IF EXISTS {table_name}")
                logger.info(f"Dropped existing table {table_name}")
            
            # Register arrow table temporarily and create DuckDB table
            self.conn.register('_temp_arrow', arrow_table)
            self.conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM _temp_arrow")
            self.conn.unregister('_temp_arrow')
            
            # Get row count
            count = self.conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
            logger.info(f"Loaded {count} rows into table '{table_name}'")
            
            # Create indexes on common columns
            if create_indexes:
                self._create_indexes(table_name)
            
        except Exception as e:
            logger.error(f"Failed to load data into {table_name}: {e}")
            raise

    def _create_indexes(self, table_name: str):
        """
        Create indexes on common key columns.
        
        Args:
            table_name: Target table name
        """
        try:
            # Get columns of the table
            columns = self.conn.execute(
                f"PRAGMA table_info('{table_name}')"
            ).fetchall()
            
            column_names = [col[1] for col in columns]
            
            # Create indexes for common key patterns
            index_columns = [
                col for col in column_names
                if col in ['order_id', 'customer_id', 'product_id', 'order_year_month']
                and col in column_names
            ]
            
            for col in index_columns:
                index_name = f"idx_{table_name}_{col}"
                try:
                    self.conn.execute(
                        f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name}({col})"
                    )
                    logger.debug(f"Created index {index_name}")
                except Exception as e:
                    logger.warning(f"Could not create index on {col}: {e}")
        
        except Exception as e:
            logger.warning(f"Error creating indexes for {table_name}: {e}")

    def load_pipeline_data(self, dataframes: Dict[str, DataFrame]):
        """
        Load all transformed dataframes from pipeline.
        
        Args:
            dataframes: Dictionary with table names and DataFrames
        """
        logger.info("Starting bulk data load into DuckDB")
        
        for table_name, df in dataframes.items():
            self.load_spark_df(df, table_name)
        
        logger.info("Bulk data load completed")

    def execute_query(self, query: str):
        """
        Execute a SQL query.
        
        Args:
            query: SQL query string
        
        Returns:
            Query result
        """
        try:
            result = self.conn.execute(query).fetchall()
            return result
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise

    def get_table_stats(self, table_name: str) -> Dict:
        """
        Get statistics about a table.
        
        Args:
            table_name: Target table name
        
        Returns:
            Dictionary with table statistics
        """
        try:
            row_count = self.conn.execute(
                f"SELECT COUNT(*) FROM {table_name}"
            ).fetchone()[0]
            
            columns = self.conn.execute(
                f"PRAGMA table_info('{table_name}')"
            ).fetchall()
            
            return {
                "table_name": table_name,
                "row_count": row_count,
                "column_count": len(columns),
                "columns": [col[1] for col in columns]
            }
        except Exception as e:
            logger.error(f"Failed to get stats for {table_name}: {e}")
            return {}

    def close(self):
        """Close DuckDB connection."""
        if self.conn:
            self.conn.close()
            logger.info("DuckDB connection closed")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
