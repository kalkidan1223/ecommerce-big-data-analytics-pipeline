"""
Airflow DAG for Data Pipeline Orchestration.
Schedules,and monitors the complete ETL process with detailed logging and error handling.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
import logging
import sys
import os
import subprocess
import shutil

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.extract import DataExtractor
from src.transform import DataTransformer
from src.load import DuckDBLoader
from src.config import (
    AIRFLOW_DAG_ID,
    PIPELINE_SCHEDULE_INTERVAL,
    PIPELINE_START_DATE
)

logger = logging.getLogger(__name__)

# Default arguments for the DAG
default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'start_date': PIPELINE_START_DATE,
    'email': ['admin@datapipeline.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(hours=2),
}

# DAG definition
dag = DAG(
    AIRFLOW_DAG_ID,
    default_args=default_args,
    description='Advanced ETL Pipeline with PySpark, DuckDB, and dbt',
    schedule_interval=PIPELINE_SCHEDULE_INTERVAL,
    catchup=False,
    tags=['data-pipeline', 'etl', 'production'],
    max_active_runs=1,
)


def extract_data(**context):
    """Extract data from all configured sources."""
    execution_date = context['execution_date']
    logger.info(f"Extracting data for execution date: {execution_date}")
    
    try:
        extractor = DataExtractor()
        data = extractor.extract_all()
        
        # Store metadata in XCom for downstream tasks
        context['task_instance'].xcom_push(
            key='extraction_timestamp',
            value=execution_date.isoformat()
        )
        
        extraction_stats = {
            'orders_count': data['orders'].count(),
            'payments_count': data['payments'].count(),
            'items_count': data['items'].count(),
        }
        
        logger.info(f"Extraction completed: {extraction_stats}")
        context['task_instance'].xcom_push(
            key='extraction_stats',
            value=extraction_stats
        )
        
        extractor.close()
        return True
    
    except Exception as e:
        logger.error(f"Extraction failed: {e}", exc_info=True)
        raise


def transform_data(**context):
    """Transform and validate extracted data."""
    logger.info("Starting data transformation...")
    
    try:
        extractor = DataExtractor()
        raw_data = extractor.extract_all()
        
        transformer = DataTransformer()
        
        # Transform individual datasets
        orders = transformer.transform_orders(raw_data['orders'])
        payments = transformer.transform_payments(raw_data['payments'])
        items = transformer.transform_items(raw_data['items'])
        
        # Create aggregated views
        order_summary = transformer.aggregate_order_summary(orders, payments, items)
        customer_metrics = transformer.create_customer_metrics(orders, payments)
        
        # Store transformation stats
        transform_stats = {
            'orders_transformed': orders.count(),
            'payments_transformed': payments.count(),
            'items_transformed': items.count(),
            'order_summary_count': order_summary.count(),
            'customer_metrics_count': customer_metrics.count(),
        }
        
        logger.info(f"Transformation completed: {transform_stats}")
        context['task_instance'].xcom_push(
            key='transform_stats',
            value=transform_stats
        )
        
        extractor.close()
        return True
    
    except Exception as e:
        logger.error(f"Transformation failed: {e}", exc_info=True)
        raise


def load_data(**context):
    """Load transformed data into DuckDB."""
    logger.info("Starting data load into DuckDB...")
    
    try:
        extractor = DataExtractor()
        raw_data = extractor.extract_all()
        
        transformer = DataTransformer()
        orders = transformer.transform_orders(raw_data['orders'])
        payments = transformer.transform_payments(raw_data['payments'])
        items = transformer.transform_items(raw_data['items'])
        order_summary = transformer.aggregate_order_summary(orders, payments, items)
        customer_metrics = transformer.create_customer_metrics(orders, payments)
        
        loader = DuckDBLoader()
        
        transformed_data = {
            'orders': orders,
            'payments': payments,
            'items': items,
            'order_summary': order_summary,
            'customer_metrics': customer_metrics
        }
        
        loader.load_pipeline_data(transformed_data)
        
        # Get table statistics
        load_stats = {}
        for table_name in transformed_data.keys():
            stats = loader.get_table_stats(table_name)
            load_stats[table_name] = stats
        
        logger.info(f"Load completed: {load_stats}")
        context['task_instance'].xcom_push(
            key='load_stats',
            value=load_stats
        )
        
        extractor.close()
        loader.close()
        return True
    
    except Exception as e:
        logger.error(f"Load failed: {e}", exc_info=True)
        raise


def _find_dbt_executable():
    """Locate the dbt executable in the current environment."""
    candidates = [
        os.environ.get('DBT_BIN'),
        shutil.which('dbt'),
        os.path.join(os.path.dirname(sys.executable), 'dbt'),
        os.path.join(os.path.dirname(sys.executable), 'dbt.exe'),
    ]

    for candidate in candidates:
        if candidate and os.path.exists(candidate):
            return candidate

    raise FileNotFoundError(
        'Could not locate dbt executable. Ensure dbt is installed in the Airflow environment.'
    )


def run_dbt_models(**context):
    """Run dbt models for advanced data modeling."""
    logger.info("Running dbt models...")
    
    dbt_project_dir = os.path.join(project_root, 'dbt', 'analytics')
    if not os.path.exists(dbt_project_dir):
        raise FileNotFoundError(f"dbt project not found at {dbt_project_dir}")

    dbt_bin = _find_dbt_executable()
    logger.info(f"Using dbt executable: {dbt_bin}")

    env = os.environ.copy()
    env['DBT_PROFILES_DIR'] = dbt_project_dir

    commands = [
        [dbt_bin, 'run', '--project-dir', dbt_project_dir, '--profiles-dir', dbt_project_dir],
        [dbt_bin, 'test', '--project-dir', dbt_project_dir, '--profiles-dir', dbt_project_dir],
    ]

    for command in commands:
        logger.info(f"Executing: {' '.join(command)}")
        result = subprocess.run(
            command,
            cwd=project_root,
            env=env,
            capture_output=True,
            text=True,
        )
        logger.info(result.stdout)
        if result.returncode != 0:
            logger.error(result.stderr)
            raise RuntimeError(
                f"dbt command failed: {' '.join(command)}\n{result.stderr}"
            )

    logger.info("dbt run and test completed successfully.")
    return True


def validate_pipeline(**context):
    """Validate pipeline execution and report results."""
    logger.info("Validating pipeline execution...")
    
    try:
        ti = context['task_instance']
        
        # Retrieve stats from previous tasks
        extract_stats = ti.xcom_pull(
            task_ids='extract_data',
            key='extraction_stats'
        )
        transform_stats = ti.xcom_pull(
            task_ids='transform_data',
            key='transform_stats'
        )
        load_stats = ti.xcom_pull(
            task_ids='load_data',
            key='load_stats'
        )
        
        validation_result = {
            'extraction': extract_stats,
            'transformation': transform_stats,
            'loading': load_stats,
            'validation_time': datetime.now().isoformat(),
        }
        
        logger.info(f"Pipeline validation report:\n{validation_result}")
        ti.xcom_push(key='validation_result', value=validation_result)
        
        return validation_result
    
    except Exception as e:
        logger.error(f"Validation failed: {e}", exc_info=True)
        raise


# Define tasks
task_extract = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    provide_context=True,
    dag=dag,
)

task_transform = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    provide_context=True,
    dag=dag,
)

task_load = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    provide_context=True,
    dag=dag,
)

task_dbt = PythonOperator(
    task_id='run_dbt_models',
    python_callable=run_dbt_models,
    provide_context=True,
    dag=dag,
)

task_validate = PythonOperator(
    task_id='validate_pipeline',
    python_callable=validate_pipeline,
    provide_context=True,
    dag=dag,
)

# Set task dependencies
task_extract >> task_transform >> task_load >> task_dbt >> task_validate
