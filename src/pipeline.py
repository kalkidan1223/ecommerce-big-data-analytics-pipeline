"""
Main pipeline orchestration module.
Coordinates the entire ETL process: Extract -> Transform -> Load
"""

import logging
import sys
from datetime import datetime
from typing import Dict

from src.extract import DataExtractor
from src.transform import DataTransformer
from src.load import DuckDBLoader
from src.config import LOG_LEVEL, LOG_FORMAT

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT
)
logger = logging.getLogger(__name__)


class DataPipeline:
    """Orchestrates the complete ETL pipeline."""

    def __init__(self):
        """Initialize pipeline components."""
        self.extractor = DataExtractor()
        self.transformer = DataTransformer()
        self.loader = DuckDBLoader()
        self.start_time = None
        self.end_time = None

    def run(self):
        """
        Execute the complete ETL pipeline.
        
        Returns:
            Dictionary with pipeline execution results
        """
        try:
            self.start_time = datetime.now()
            logger.info("=" * 80)
            logger.info(f"Starting Data Pipeline - {self.start_time}")
            logger.info("=" * 80)
            
            # Step 1: Extract data from all sources
            logger.info("\n[STEP 1] EXTRACTION")
            logger.info("-" * 80)
            raw_data = self._extract_phase()
            
            # Step 2: Transform extracted data
            logger.info("\n[STEP 2] TRANSFORMATION")
            logger.info("-" * 80)
            transformed_data = self._transform_phase(raw_data)
            
            # Step 3: Load into DuckDB
            logger.info("\n[STEP 3] LOAD")
            logger.info("-" * 80)
            self._load_phase(transformed_data)
            
            # Step 4: Generate summary
            logger.info("\n[STEP 4] VALIDATION & SUMMARY")
            logger.info("-" * 80)
            summary = self._generate_summary()
            
            self.end_time = datetime.now()
            duration = (self.end_time - self.start_time).total_seconds()
            
            logger.info("=" * 80)
            logger.info(f"Pipeline completed successfully in {duration:.2f} seconds")
            logger.info("=" * 80)
            
            return {
                "status": "SUCCESS",
                "start_time": self.start_time,
                "end_time": self.end_time,
                "duration_seconds": duration,
                "summary": summary
            }
        
        except Exception as e:
            logger.error(f"Pipeline failed: {e}", exc_info=True)
            return {
                "status": "FAILED",
                "error": str(e),
                "start_time": self.start_time
            }
        
        finally:
            self.cleanup()

    def _extract_phase(self) -> Dict:
        """Extract data from all sources."""
        logger.info("Extracting data from configured sources...")
        raw_data = self.extractor.extract_all()
        
        for name, df in raw_data.items():
            logger.info(f"  - {name}: {df.count()} records, {len(df.columns)} columns")
        
        return raw_data

    def _transform_phase(self, raw_data: Dict) -> Dict:
        """Transform extracted data."""
        logger.info("Applying business logic transformations...")
        
        # Transform individual datasets
        orders = self.transformer.transform_orders(raw_data["orders"])
        payments = self.transformer.transform_payments(raw_data["payments"])
        items = self.transformer.transform_items(raw_data["items"])
        
        logger.info("Creating aggregated views...")
        
        # Create aggregated views for analytics
        order_summary = self.transformer.aggregate_order_summary(
            orders, payments, items
        )
        customer_metrics = self.transformer.create_customer_metrics(
            orders, payments
        )
        
        transformed_data = {
            "orders": orders,
            "payments": payments,
            "items": items,
            "order_summary": order_summary,
            "customer_metrics": customer_metrics
        }
        
        for name, df in transformed_data.items():
            logger.info(f"  - {name}: {df.count()} records prepared")
        
        return transformed_data

    def _load_phase(self, transformed_data: Dict):
        """Load transformed data into DuckDB."""
        logger.info("Loading data into DuckDB...")
        self.loader.load_pipeline_data(transformed_data)

    def _generate_summary(self) -> Dict:
        """Generate pipeline execution summary."""
        logger.info("Generating pipeline summary...")
        
        summary = {}
        for table in ["orders", "payments", "items", "order_summary", "customer_metrics"]:
            try:
                stats = self.loader.get_table_stats(table)
                summary[table] = stats
                if stats:
                    logger.info(
                        f"  - {table}: {stats['row_count']} rows, "
                        f"{stats['column_count']} columns"
                    )
            except Exception as e:
                logger.warning(f"Could not get stats for {table}: {e}")
        
        return summary

    def cleanup(self):
        """Clean up resources."""
        logger.info("Cleaning up resources...")
        self.extractor.close()
        self.loader.close()


def main():
    """Main entry point."""
    pipeline = DataPipeline()
    result = pipeline.run()
    
    # Exit with appropriate code
    sys.exit(0 if result["status"] == "SUCCESS" else 1)


if __name__ == "__main__":
    main()
