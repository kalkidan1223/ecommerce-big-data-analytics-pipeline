# Big Data Analytics Pipeline for E-Commerce Data

This project implements an end-to-end data analytics pipeline for the Brazilian Olist e-commerce dataset. It extracts raw order, payment, and item data, transforms it with PySpark, stores analytical tables in DuckDB, supports dbt-based modeling, and exports CSV files for Power BI reporting.

The solution was developed as a big data analytics project by Group 5.

## Repository Name

```text
bigdata-analytics-project
```

## Table of Contents

- [Repository Name](#repository-name)
- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Dataset](#dataset)
- [Pipeline Output](#pipeline-output)
- [Power BI Dashboard](#power-bi-dashboard)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [How to Run](#how-to-run)
- [dbt Configuration](#dbt-configuration)
- [Airflow Orchestration](#airflow-orchestration)
- [Group Members](#group-members)

## Project Overview

The goal of this project is to build a reliable analytics workflow that converts raw e-commerce transaction data into clean, structured, and analysis-ready datasets.

The pipeline performs the following tasks:

- Extracts data from CSV and Parquet source files.
- Cleans and transforms orders, payments, and order item records.
- Creates aggregated analytical tables such as order summaries and customer metrics.
- Loads processed data into DuckDB for fast local analytics.
- Supports dbt modeling and testing.
- Exports Power BI-ready CSV files for dashboard development.

## Architecture

```text
Raw Data Sources
    |
    |-- olist_orders_dataset.csv
    |-- olist_order_payments_dataset.csv
    |-- olist_order_items_dataset.parquet
    |
    v
PySpark ETL Pipeline
    |
    |-- Extraction
    |-- Cleaning and transformation
    |-- Aggregation
    |
    v
DuckDB Analytics Database
    |
    |-- orders
    |-- payments
    |-- items
    |-- order_summary
    |-- customer_metrics
    |
    v
dbt Models and Tests
    |
    v
Power BI CSV Exports and Dashboards
```

## Technology Stack

| Component | Technology | Purpose |
| --- | --- | --- |
| Programming language | Python | Main pipeline implementation |
| Distributed processing | PySpark | Data extraction and transformation |
| Analytical database | DuckDB | Local OLAP storage |
| Data modeling | dbt | SQL models, testing, and documentation |
| Workflow orchestration | Apache Airflow | Pipeline scheduling and monitoring |
| Business intelligence | Power BI | Dashboard and reporting |
| Data formats | CSV, Parquet | Raw and exported datasets |

## Dataset

The project uses selected tables from the Olist Brazilian e-commerce dataset.

| Source file | Description |
| --- | --- |
| `data/raw/olist_orders_dataset.csv` | Order-level information including order status, customer ID, purchase date, and delivery dates |
| `data/raw/olist_order_payments_dataset.csv` | Payment details including payment type, installments, and payment value |
| `data/raw/olist_order_items_dataset.parquet` | Item-level details including product, seller, price, and freight value |

## Pipeline Output

After running the pipeline, the processed DuckDB database is created at:

```text
data/processed/analytics.duckdb
```

The main analytical tables are:

| Table | Description |
| --- | --- |
| `orders` | Cleaned order records |
| `payments` | Cleaned payment records |
| `items` | Cleaned order item records |
| `order_summary` | Order-level aggregated metrics |
| `customer_metrics` | Customer-level analytical metrics |

Power BI-ready CSV exports are available in:

```text
data/powerbi/
```

Available CSV files:

- `order_summary.csv`
- `customer_metrics.csv`
- `orders.csv`
- `payments.csv`
- `items.csv`

To regenerate these CSV files, run:

```powershell
venv\Scripts\python.exe scripts\export_powerbi_csv.py
```

## Power BI Dashboard

The Power BI dashboard uses the exported CSV files to analyze sales performance, freight cost, payment behavior, and time-series trends.

### Dashboard Screenshots

![Power BI Sales and Freight Dashboard](<dashboard/screenshots/Power BI Sales&FreightDashboard.png>)

![Time-Series Sales Analysis in Power BI](<dashboard/screenshots/Time-Series Sales Analysis in Power BI.png>)

![Payment Type Analysis Dashboard](<dashboard/screenshots/Payment Type Analysis Dashboard.png>)

Recommended file to load first in Power BI:

```text
data/powerbi/order_summary.csv
```

## Project Structure

```text
bigdata-analytics-project/
|-- airflow/
|   |-- dags/
|   |   `-- data_pipeline_dag.py
|   `-- airflow.cfg
|-- config/
|-- dashboard/
|   `-- screenshots/
|-- data/
|   |-- raw/
|   |-- processed/
|   `-- powerbi/
|-- dbt/
|   `-- analytics/
|       |-- dbt_project.yml
|       |-- profiles.yml
|       `-- models/
|-- scripts/
|   `-- export_powerbi_csv.py
|-- sql/
|-- src/
|   |-- config.py
|   |-- extract.py
|   |-- transform.py
|   |-- load.py
|   `-- pipeline.py
|-- requirements.txt
`-- README.md
```

## Setup Instructions

### 1. Create a virtual environment

```powershell
python -m venv venv
```

### 2. Activate the virtual environment

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Confirm required source data

Make sure the following files exist in `data/raw/`:

```text
olist_orders_dataset.csv
olist_order_payments_dataset.csv
olist_order_items_dataset.parquet
```

## How to Run

Run the full ETL pipeline from the project root:

```powershell
python -m src.pipeline
```

The pipeline performs extraction, transformation, loading, and validation. A successful run creates or updates:

```text
data/processed/analytics.duckdb
```

Then export CSV files for Power BI:

```powershell
venv\Scripts\python.exe scripts\export_powerbi_csv.py
```

## dbt Configuration

The dbt project is located in:

```text
dbt/analytics/
```

The DuckDB profile points to the processed database:

```yaml
path: '../../data/processed/analytics.duckdb'
```

Run dbt commands from the `dbt/analytics` directory:

```powershell
cd dbt/analytics
dbt debug
dbt run
dbt test
```

If DuckDB returns an `Access is denied` error, close any Python, dbt, Airflow, or notebook process that may still be using `analytics.duckdb`.

## Airflow Orchestration

The Airflow DAG is defined at:

```text
airflow/dags/data_pipeline_dag.py
```

It can be used to schedule and monitor the pipeline workflow. The DAG coordinates the pipeline tasks and allows repeatable execution through the Airflow interface.

## Group Members

Group 5:

| No. | Name |
| --- | --- |
| 1 | KALKIDAN AMBAW |
| 2 | SELAMAWIT ASFAW |
| 3 | MIHRET ABEBE |
| 4 | ETUSBDINK MEKETE |
| 5 | LEUL TEKESTE |
| 6 | SAMRAWIT GEBRETENSAY |
| 7 | FIREZER SETTUAL |
| 8 | SHEGAW AFELE |
| 9 | ZEREYAKOB DEREJE |

## Conclusion
This project demonstrates a complete data engineering and analytics workflow using modern tools for data processing, storage, modeling, orchestration, and visualization. The final outputs are suitable for business intelligence reporting and further analytical exploration in Power BI.
