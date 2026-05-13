# Architecture Diagram

## High-Level Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        DATA PIPELINE ARCHITECTURE                       │
└─────────────────────────────────────────────────────────────────────────┘

LAYER 1: DATA SOURCES
═══════════════════════════════════════════════════════════════════════════
┌──────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                  │
│  │   CSV File   │  │   CSV File   │  │ Parquet File │                  │
│  │   Orders    │  │   Payments   │  │    Items     │                  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘                  │
│         │                  │                  │                          │
└─────────┼──────────────────┼──────────────────┼──────────────────────────┘
          │                  │                  │

LAYER 2: ORCHESTRATION LAYER (Apache Airflow)
═══════════════════════════════════════════════════════════════════════════
┌──────────────────────────────────────────────────────────────────────────┐
│                         AIRFLOW DAG                                      │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                                                                    │ │
│  │  START → EXTRACT → TRANSFORM → LOAD → DBT → VALIDATE → END      │ │
│  │    ↑                                                         ↓     │ │
│  │    └──────────────── RETRY LOGIC ──────────────────────────┘     │ │
│  │                                                                    │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
│  Task Scheduling: Daily at 2:00 AM UTC                                  │
│  Error Handling: Retry 1x after 5 min delay                             │
│  Max Runtime: 2 hours per pipeline execution                            │
└──────────────────────────────────────────────────────────────────────────┘

LAYER 3: PROCESSING LAYER (Apache PySpark)
═══════════════════════════════════════════════════════════════════════════
┌──────────────────────────────────────────────────────────────────────────┐
│                      PYSPARK EXECUTION ENGINE                            │
│                                                                          │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐          │
│  │   EXTRACT    │      │  TRANSFORM   │      │    LOAD      │          │
│  ├──────────────┤      ├──────────────┤      ├──────────────┤          │
│  │ • Read CSV   │ ───→ │ • Clean Data │ ───→ │ • Arrow Conv │          │
│  │ • Read       │      │ • Validate   │      │ • Create     │          │
│  │   Parquet    │      │ • Enrich     │      │   Tables     │          │
│  │ • Schema     │      │ • Aggregate  │      │ • Index      │          │
│  │   Inference  │      │ • Derive     │      │ • Validate   │          │
│  │ • Validation │      │   Metrics    │      │   Output     │          │
│  └──────────────┘      └──────────────┘      └──────────────┘          │
│                                                                          │
│  Memory Config: local[*]     Performance: Adaptive Query Optimization   │
│  Partitions: 8 shuffle       Data Format: Arrow (efficient columnar)    │
└──────────────────────────────────────────────────────────────────────────┘

LAYER 4: DATA WAREHOUSE LAYER (DuckDB)
═══════════════════════════════════════════════════════════════════════════
┌──────────────────────────────────────────────────────────────────────────┐
│                   DUCKDB ANALYTICS DATABASE                              │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                      Raw Tables                                  │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐                       │  │
│  │  │ orders   │  │ payments │  │  items   │                       │  │
│  │  └──────────┘  └──────────┘  └──────────┘                       │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                           ↓ (dbt models)                                │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                    Staging Layer (Views)                         │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │  │
│  │  │ stg_orders   │  │ stg_payments │  │ stg_items    │           │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘           │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                           ↓ (dbt models)                                │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │              Mart Layer (Analytics Tables)                       │  │
│  │  ┌──────────────────────┐  ┌──────────────────────┐             │  │
│  │  │  fct_orders (Fact)   │  │  dim_customers       │             │  │
│  │  │ - Order details      │  │ - Customer metrics   │             │  │
│  │  │ - Aggregations       │  │ - Segmentation       │             │  │
│  │  └──────────────────────┘  └──────────────────────┘             │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  Storage: Columnar OLAP format                                          │
│  Indexing: Auto-index on order_id, customer_id, product_id             │
│  Features: ACID transactions, sub-second query response                │
└──────────────────────────────────────────────────────────────────────────┘

LAYER 5: ANALYTICS & BI LAYER (Power BI)
═══════════════════════════════════════════════════════════════════════════
┌──────────────────────────────────────────────────────────────────────────┐
│                         POWER BI DASHBOARDS                              │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Executive Summary  │  Order Analytics  │  Customer Insights    │   │
│  ├─────────────────────┼──────────────────┼──────────────────────┤   │
│  │ • Revenue Trends    │ • Status Report  │ • Segmentation       │   │
│  │ • KPI Cards         │ • Fulfillment    │ • Lifetime Value     │   │
│  │ • Customer Count    │ • Value Segments │ • Churn Analysis     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  Connected via ODBC: DuckDB → Power BI (Direct Query or Import)        │
│  Refresh Schedule: Daily at 3:00 AM UTC (after pipeline completion)    │
│  Access: Web & Desktop versions available                               │
└──────────────────────────────────────────────────────────────────────────┘


DATA FLOW DIAGRAM
═══════════════════════════════════════════════════════════════════════════

Raw Data Sources
    ↓
[Orders CSV] ──┐
[Payments CSV]─┼──→ [PySpark Extractor] → [Raw DataFrames]
[Items Parquet]┘                              ↓
                                        [Transformer]
                                        (Clean, Validate)
                                              ↓
                                        [Aggregator]
                                        (Create Views)
                                              ↓
                                        [DuckDB Loader]
                                              ↓
                                    [DuckDB Database]
                                    (Raw Tables)
                                              ↓
                                        [dbt Models]
                                        (Staging views)
                                              ↓
                                        [dbt Models]
                                        (Mart tables)
                                              ↓
                                    [Analytics Tables]
                                    (fct_orders, dim_customers)
                                              ↓
                                        [Power BI]
                                        (Visualizations)


DEPENDENCY GRAPH
═══════════════════════════════════════════════════════════════════════════

orders.csv
    ↓
stg_orders (dbt) ──┐
                   ├──→ fct_orders (dbt) ──┐
stg_items (dbt) ───┤                       ├──→ dim_customers (dbt)
                   │                       │
stg_payments (dbt)─┴───→ (aggregations) ──┘


KEY DESIGN PATTERNS
═══════════════════════════════════════════════════════════════════════════

1. SEPARATION OF CONCERNS
   - Extract: Focus on data reading
   - Transform: Focus on business logic
   - Load: Focus on persistence

2. LAYERED ARCHITECTURE
   - Staging: Clean, validated data
   - Mart: Business-ready dimensions & facts
   - (Follows dimensional modeling best practices)

3. IDEMPOTENCY
   - All transformations are re-runnable
   - Overwrite mode for safety
   - No duplicates in fact/dimension tables

4. QUALITY ASSURANCE
   - Data validation at each step
   - dbt tests for data integrity
   - Comprehensive logging

5. SCALABILITY
   - PySpark for distributed processing
   - DuckDB for analytical queries
   - Airflow for workflow management


PERFORMANCE CHARACTERISTICS
═══════════════════════════════════════════════════════════════════════════

Data Volume (Current):
  • Orders: 100,000 records
  • Payments: 150,000 records
  • Items: 200,000 records
  • Total: ~450,000 records

Processing Performance:
  • Extraction: ~5-10 seconds
  • Transformation: ~20-30 seconds
  • Loading: ~5-10 seconds
  • dbt models: ~10-15 seconds
  • Total pipeline: ~45-60 seconds

Query Performance (DuckDB):
  • Revenue by month: <100ms
  • Customer metrics: <500ms
  • Complex aggregations: <1s

Storage:
  • DuckDB database: ~50MB (compressed)
  • Full analytics load: ~100MB


MONITORING & OBSERVABILITY
═══════════════════════════════════════════════════════════════════════════

Airflow Monitoring:
  • DAG execution history
  • Task success/failure rates
  • Task duration tracking
  • Log aggregation

Data Quality Monitoring:
  • Row count validation
  • dbt test results
  • Schema change detection
  • Data freshness checks

Application Logging:
  • Python logging to files
  • INFO/DEBUG/ERROR levels
  • Timestamps for debugging
