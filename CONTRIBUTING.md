# Contributing Guidelines

## Team Structure & Contributions

This advanced ETL project was designed and implemented by a collaborative data engineering team with specialized expertise across the stack.

### 👥 Team Members & Primary Contributions

#### **1. Project Lead / Senior Data Architect**
**Role**: Architecture design and project coordination

**Primary Contributions**:
- Overall pipeline architecture design
- Technology stack selection (PySpark, DuckDB, Airflow)
- System integration and orchestration planning
- Quality assurance and performance optimization
- Documentation and README development

**Key Files/Components**:
- `README.md` - Comprehensive project documentation
- `docs/architecture/ARCHITECTURE.md` - System design
- `src/config.py` - Central configuration management
- `src/pipeline.py` - Pipeline orchestration
- Project structure and organization

---

#### **2. PySpark & ETL Engineer**
**Role**: Data extraction, transformation, and pipeline development

**Primary Contributions**:
- Designed and implemented data extraction module
- Developed data transformation logic with business rules
- Implemented data quality validation
- Created aggregation and metric calculations
- Built Airflow DAG for pipeline orchestration

**Key Files/Components**:
- `src/extract.py` - Multi-source data extraction
  - CSV file reading
  - Parquet file parsing
  - Schema inference
  - Data validation
- `src/transform.py` - Data transformation logic
  - Orders cleaning and enrichment
  - Payments standardization
  - Items aggregation
  - Metric calculations
- `airflow/dags/data_pipeline_dag.py` - Complete workflow orchestration
  - Extract tasks
  - Transform tasks
  - Load tasks
  - Error handling and retries
  - Logging and monitoring
- `requirements.txt` - Python dependencies

**Technologies**:
- Apache PySpark for distributed processing
- PySpark SQL for transformations
- Python 3.9+

---

#### **3. Database & Data Modeling Engineer**
**Role**: DuckDB setup, dbt modeling, data warehouse design

**Primary Contributions**:
- Implemented DuckDB loading mechanism
- Designed and built dbt transformation models
- Created staging and mart layers
- Implemented data quality tests
- Optimized database performance with indexing

**Key Files/Components**:
- `src/load.py` - DuckDB data loading
  - PySpark to Arrow conversion
  - Table creation and management
  - Index creation
  - Database optimization
- `dbt/analytics/dbt_project.yml` - dbt project configuration
- `dbt/analytics/profiles.yml` - Database connection profile
- **Staging Models** (Cleaning & Validation):
  - `dbt/analytics/models/staging/stg_orders.sql`
  - `dbt/analytics/models/staging/stg_payments.sql`
  - `dbt/analytics/models/staging/stg_items.sql`
- **Mart Models** (Analytics-ready tables):
  - `dbt/analytics/models/marts/core/fct_orders.sql` - Fact table
  - `dbt/analytics/models/marts/core/dim_customers.sql` - Dimension table
- **Data Quality Tests**:
  - `dbt/analytics/tests/test_stg_orders.sql`
  - `dbt/analytics/tests/test_stg_payments.sql`

**Technologies**:
- DuckDB for analytical database
- dbt for SQL-based transformations
- Data modeling best practices

---

#### **4. Analytics & Business Intelligence Engineer**
**Role**: BI dashboard development, analytics queries, insights generation

**Primary Contributions**:
- Designed Power BI dashboard architecture
- Wrote SQL analytics queries
- Created business metrics and KPIs
- Documented BI connection procedures
- Built visualization specifications

**Key Files/Components**:
- `sql/analytics_queries.sql` - Pre-built analytics queries
  - Revenue analysis by month
  - Customer segmentation
  - Order status distribution
  - Delivery performance metrics
  - Payment method analysis
  - Customer activity tracking
- `docs/POWERBI_SETUP.md` - Power BI connection guide
  - ODBC driver installation
  - DSN configuration
  - Power BI desktop connection
  - Dashboard design patterns
  - Example visualizations
- `dashboard/powerbi/` - Power BI reports and dashboards
- Dashboard specifications and mockups

**Technologies**:
- Power BI Desktop and Service
- SQL for data analysis
- DAX for calculated measures
- ODBC for database connectivity

---

## Contribution Areas

### Infrastructure & DevOps

| File/Component | Owner | Purpose |
|---|---|---|
| `docker-compose.yml` | Project Lead | Container orchestration |
| `Dockerfile.airflow` | PySpark Engineer | Airflow containerization |
| `setup.ps1` | Project Lead | Windows environment setup |
| `setup.sh` | Project Lead | Unix environment setup |
| `Makefile` | Project Lead | Development commands |
| `.env.example` | Project Lead | Configuration template |
| `.gitignore` | Project Lead | Version control rules |

### Configuration

| File/Component | Owner | Purpose |
|---|---|---|
| `src/config.py` | Project Lead | Central configuration |
| `airflow/airflow.cfg` | PySpark Engineer | Airflow settings |
| `dbt/analytics/dbt_project.yml` | DB Engineer | dbt configuration |
| `dbt/analytics/profiles.yml` | DB Engineer | Database connection |
| `requirements.txt` | PySpark Engineer | Python dependencies |
| `pytest.ini` | QA Team | Test configuration |

### Documentation

| File/Component | Owner | Purpose |
|---|---|---|
| `README.md` | Project Lead | Main documentation |
| `QUICKSTART.md` | Project Lead | Quick start guide |
| `docs/architecture/ARCHITECTURE.md` | Project Lead | Architecture diagrams |
| `docs/POWERBI_SETUP.md` | Analytics Engineer | BI setup guide |
| `CONTRIBUTING.md` | Project Lead | This file |

---

## Development Workflow

### Code Organization

```
src/                        # Core ETL modules
├── config.py              # Configuration (Project Lead)
├── extract.py             # Extraction logic (PySpark Engineer)
├── transform.py           # Transformation logic (PySpark Engineer)
├── load.py                # Loading logic (DB Engineer)
└── pipeline.py            # Orchestration (PySpark Engineer)

airflow/dags/              # Workflow orchestration
└── data_pipeline_dag.py   # Main DAG (PySpark Engineer)

dbt/analytics/             # Data modeling
├── models/
│   ├── staging/          # Staging views (DB Engineer)
│   └── marts/            # Mart tables (DB Engineer)
└── tests/                # Data quality (DB Engineer)

sql/                       # Analytics queries
└── analytics_queries.sql  # BI queries (Analytics Engineer)

docs/                      # Documentation
├── architecture/
│   └── ARCHITECTURE.md    # Architecture (Project Lead)
└── POWERBI_SETUP.md      # BI guide (Analytics Engineer)
```

---

## Key Technologies & Assignments

| Technology | Primary Owner | Secondary |
|-----------|---------------|-----------|
| **PySpark** | PySpark Engineer | Project Lead |
| **DuckDB** | DB Engineer | PySpark Engineer |
| **Airflow** | PySpark Engineer | Project Lead |
| **dbt** | DB Engineer | Analytics Engineer |
| **Power BI** | Analytics Engineer | DB Engineer |
| **Python/SQL** | All members | All members |
| **Architecture** | Project Lead | All members |
| **Documentation** | Project Lead | All members |
| **DevOps/Docker** | Project Lead | PySpark Engineer |

---

## How to Contribute

### 1. Feature Development

1. **Create a branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes** in your area:
   - PySpark Engineer: Modify `src/extract.py` or `src/transform.py`
   - DB Engineer: Update dbt models or `src/load.py`
   - Analytics Engineer: Add queries or Power BI configurations
   - Project Lead: Coordinate and update architecture

3. **Test your changes**:
   ```bash
   pytest tests/
   ```

4. **Commit with clear messages**:
   ```bash
   git commit -m "feat: add [feature description]"
   ```

5. **Create Pull Request**:
   - Describe changes
   - Reference related issues
   - Request review from relevant engineer

### 2. Code Review Process

- **Owner review**: Primary owner of component reviews
- **Secondary review**: Cross-team validation
- **Merge**: At least 1 approval required
- **Tests**: All tests must pass

### 3. Documentation Updates

When contributing code:
- Update relevant docstrings
- Add inline comments for complex logic
- Update README if behavior changes
- Document new configuration options

---

## Performance Responsibilities

### PySpark Engineer
- Monitor Spark job performance
- Optimize transformation logic
- Handle data quality issues
- Troubleshoot pipeline failures

### DB Engineer
- Monitor DuckDB query performance
- Optimize indexes and materialization
- Maintain dbt test suites
- Ensure data consistency

### Analytics Engineer
- Monitor dashboard performance
- Optimize Power BI queries
- Respond to business questions
- Create new analytics views

### Project Lead
- Overall system monitoring
- Coordinate between teams
- Manage dependencies and releases
- Ensure documentation is current

---

## Testing & Quality Assurance

### Unit Tests
```bash
pytest tests/unit/
```

### Integration Tests
```bash
pytest tests/integration/
```

### Data Quality Tests (dbt)
```bash
cd dbt/analytics
dbt test
```

### linting
```bash
black src/
flake8 src/
```

---

## Release Process

1. **Feature Branch**: Develop and test
2. **Code Review**: Team review
3. **Integration Testing**: Full pipeline test
4. **Documentation**: Update all docs
5. **Version Bump**: Update version in code
6. **Release**: Merge to main branch
7. **Deployment**: Deploy to production

---

## Troubleshooting & Support

### Common Issues

| Issue | Owner | Solution |
|-------|-------|----------|
| Spark Job Fails | PySpark Engineer | Check spark config, memory settings |
| DuckDB Connection Error | DB Engineer | Verify ODBC driver, database path |
| dbt Model Error | DB Engineer | Debug with `dbt debug`, check SQL |
| Airflow DAG Issues | PySpark Engineer | Validate DAG syntax, check imports |
| Power BI Connection | Analytics Engineer | Check ODBC DSN, firewall rules |

### Getting Help

1. **Check logs**:
   - Airflow: `airflow/logs/`
   - PySpark: Console output
   - dbt: `dbt/analytics/logs/`

2. **Contact relevant owner**:
   - PySpark issues → PySpark Engineer
   - Database issues → DB Engineer
   - BI issues → Analytics Engineer
   - General questions → Project Lead

3. **Review documentation**:
   - README.md for overview
   - ARCHITECTURE.md for design
   - POWERBI_SETUP.md for BI details

---

## Communication

### Team Meetings
- **Daily**: 15-min standup (9:00 AM)
- **Weekly**: 1-hour sync (Thursday 2:00 PM)
- **As-needed**: Technical deep dives

### Escalation Path
1. Team member with relevant expertise
2. Engineering lead
3. Project lead for major decisions

---

## Version History

| Version | Date | Authors | Summary |
|---------|------|---------|---------|
| 1.0.0 | Jan 2024 | All | Initial release with all core features |

---

## License & Attribution

This project incorporates components and patterns from:
- Apache Spark documentation
- DuckDB examples
- dbt best practices
- Airflow tutorials

All original code is credited to the team members listed above.

---

**Thank you for contributing to this project!** 🚀
