"""
Transform module for data quality and business logic transformations.
Handles cleaning, validation, and enrichment of extracted data.
"""

import logging
from typing import Dict
from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    col, to_date, when, coalesce, sum as spark_sum,
    count, avg, min as spark_min, max as spark_max,
    year, month, dayofmonth, date_format, lit
)
from pyspark.sql.window import Window

logger = logging.getLogger(__name__)


class DataTransformer:
    """Transforms and cleanses data according to business rules."""

    @staticmethod
    def transform_orders(orders_df: DataFrame) -> DataFrame:
        """
        Transform orders data.
        - Clean null values
        - Standardize date formats
        - Create derived columns
        
        Args:
            orders_df: Raw orders DataFrame
        
        Returns:
            Transformed orders DataFrame
        """
        logger.info("Transforming orders data")
        
        df = orders_df \
            .dropna(subset=["order_id", "customer_id"]) \
            .withColumn("order_purchase_timestamp", 
                       to_date(col("order_purchase_timestamp"), "yyyy-MM-dd HH:mm:ss")) \
            .withColumn("order_approved_at",
                       to_date(col("order_approved_at"), "yyyy-MM-dd HH:mm:ss")) \
            .withColumn("order_delivered_carrier_date",
                       to_date(col("order_delivered_carrier_date"), "yyyy-MM-dd HH:mm:ss")) \
            .withColumn("order_delivered_customer_date",
                       to_date(col("order_delivered_customer_date"), "yyyy-MM-dd HH:mm:ss")) \
            .withColumn("order_estimated_delivery_date",
                       to_date(col("order_estimated_delivery_date"), "yyyy-MM-dd HH:mm:ss"))
        
        # Create year-month for easier aggregations
        df = df.withColumn("order_year_month", 
                          date_format(col("order_purchase_timestamp"), "yyyy-MM"))
        
        # Clean order status
        df = df.withColumn("order_status", 
                          col("order_status").cast("string"))
        
        logger.info(f"Transformed {df.count()} order records")
        return df

    @staticmethod
    def transform_payments(payments_df: DataFrame) -> DataFrame:
        """
        Transform payments data.
        - Clean numeric values
        - Standardize payment types
        - Handle missing values
        
        Args:
            payments_df: Raw payments DataFrame
        
        Returns:
            Transformed payments DataFrame
        """
        logger.info("Transforming payments data")
        
        df = payments_df \
            .dropna(subset=["order_id"]) \
            .withColumn("payment_value", col("payment_value").cast("double"))
        
        # Standardize payment type
        df = df.withColumn("payment_type", 
                          col("payment_type").cast("string"))
        
        # Handle missing installments
        df = df.withColumn("payment_installments",
                          coalesce(col("payment_installments"), lit(1)))
        
        logger.info(f"Transformed {df.count()} payment records")
        return df

    @staticmethod
    def transform_items(items_df: DataFrame) -> DataFrame:
        """
        Transform order items data.
        - Clean numeric values
        - Standardize product categories
        - Calculate derived metrics
        
        Args:
            items_df: Raw items DataFrame
        
        Returns:
            Transformed items DataFrame
        """
        logger.info("Transforming items data")
        
        df = items_df \
            .dropna(subset=["order_id", "product_id"]) \
            .withColumn("price", col("price").cast("double")) \
            .withColumn("freight_value", col("freight_value").cast("double"))
        
        # Create item value column
        df = df.withColumn("item_total_value",
                          col("price") + coalesce(col("freight_value"), lit(0)))
        
        logger.info(f"Transformed {df.count()} item records")
        return df

    @staticmethod
    def aggregate_order_summary(
        orders_df: DataFrame,
        payments_df: DataFrame,
        items_df: DataFrame
    ) -> DataFrame:
        """
        Create order summary with aggregated metrics.
        
        Args:
            orders_df: Transformed orders data
            payments_df: Transformed payments data
            items_df: Transformed items data
        
        Returns:
            Order summary DataFrame
        """
        logger.info("Creating order summary aggregations")
        
        # Aggregate payments
        payment_summary = payments_df.groupBy("order_id") \
            .agg(
                spark_sum("payment_value").alias("total_payment"),
                count("*").alias("num_payment_methods")
            )
        
        # Aggregate items
        items_summary = items_df.groupBy("order_id") \
            .agg(
                count("*").alias("num_items"),
                spark_sum("price").alias("total_item_price"),
                spark_sum("freight_value").alias("total_freight"),
                spark_sum("item_total_value").alias("total_item_value")
            )
        
        # Combine with orders
        order_summary = orders_df \
            .join(payment_summary, "order_id", "left") \
            .join(items_summary, "order_id", "left")
        
        # Fill nulls with 0
        order_summary = order_summary.fillna(0, subset=[
            "total_payment", "num_payment_methods",
            "num_items", "total_item_price", "total_freight", "total_item_value"
        ])
        
        logger.info(f"Created summary for {order_summary.count()} orders")
        return order_summary

    @staticmethod
    def create_customer_metrics(
        orders_df: DataFrame,
        payments_df: DataFrame
    ) -> DataFrame:
        """
        Create customer-level metrics for BI analysis.
        
        Args:
            orders_df: Transformed orders data
            payments_df: Transformed payments data
        
        Returns:
            Customer metrics DataFrame
        """
        logger.info("Creating customer metrics")
        
        # Join orders with payments
        combined = orders_df.join(
            payments_df.groupBy("order_id").agg(
                spark_sum("payment_value").alias("order_total")
            ),
            "order_id"
        )
        
        # Aggregate by customer
        customer_metrics = combined.groupBy("customer_id") \
            .agg(
                count("order_id").alias("total_orders"),
                spark_sum("order_total").alias("lifetime_value"),
                avg("order_total").alias("avg_order_value"),
                spark_min("order_purchase_timestamp").alias("first_order_date"),
                spark_max("order_purchase_timestamp").alias("last_order_date")
            )
        
        logger.info(f"Created metrics for {customer_metrics.count()} customers")
        return customer_metrics
