# Quick Start Guide

Get up and running with the Data Pipeline in 5 minutes!

## 📋 Prerequisites

- Python 3.9+
- Git
- 2GB+ available RAM
- Windows 10+, macOS 10.14+, or Linux with bash

## ⚡ Quick Start (Windows)

### 1. Clone & Navigate
```bash
cd bigdata-analytics-project
```

### 2. Run Setup Script
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\setup.ps1
```

### 3. Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Run Pipeline
```bash
python -m src.pipeline
```

**Done!** Your data is now in DuckDB. ✅

---

## ⚡ Quick Start (macOS/Linux)

### 1. Clone & Navigate
```bash
cd bigdata-analytics-project
```

### 2. Run Setup Script
```bash
chmod +x setup.sh
./setup.sh
```

### 3. Activate Virtual Environment
```bash
source venv/bin/activate
```

### 4. Run Pipeline
```bash
python -m src.pipeline
```

**Done!** Your data is now in DuckDB. ✅

---

## 🚀 Next Steps

### Option A: Use Airflow for Scheduled Execution
```bash
# Terminal 1: Start Scheduler
set AIRFLOW_HOME=./airflow
airflow scheduler

# Terminal 2: Start Webserver (in another terminal)
set AIRFLOW_HOME=./airflow
airflow webserver --port 8080

# Access UI: http://localhost:8080
# Username: admin, Password: admin
```

### Option B: Use dbt for Data Transformation
```bash
cd dbt/analytics
dbt run
dbt test
```

### Option C: Connect to Power BI
1. Install DuckDB ODBC driver
2. Create ODBC data source for `data/processed/analytics.duckdb`
3. Open Power BI → Get Data → ODBC
4. Create visualizations from the tables

---

## 📊 Verify Success

Check if pipeline completed successfully:

```bash
# List DuckDB tables
python -c "import duckdb; conn = duckdb.connect('data/processed/analytics.duckdb'); 
conn.execute('SELECT table_name FROM information_schema.tables').show()"

# Expected output should show:
# - orders
# - payments  
# - items
# - order_summary
# - customer_metrics
```

---

## 📂 Key Files & Directories

| Path | Purpose |
|------|---------|
| `src/` | Core ETL Python modules |
| `airflow/dags/` | Airflow workflow definitions |
| `dbt/analytics/` | Data modeling with dbt |
| `data/raw/` | Source data files |
| `data/processed/` | DuckDB analytics database |
| `sql/` | Analytics queries |
| `README.md` | Comprehensive documentation |

---

## 🔧 Common Commands

```bash
# Run complete pipeline
python -m src.pipeline

# Start Airflow
export AIRFLOW_HOME=./airflow
airflow scheduler &
airflow webserver --port 8080

# Run dbt
cd dbt/analytics
dbt run --select staging
dbt test

# Install new packages
pip install <package-name>

# Clean cache
make clean

# Show help
make help
```

---

## ❓ Troubleshooting

### "ModuleNotFoundError: No module named 'pyspark'"
```bash
pip install -r requirements.txt
```

### "DuckDB database not found"
```bash
# Re-run the pipeline to create database
python -m src.pipeline
```

### Airflow DAG not appearing
```bash
# Check DAG syntax
airflow dags validate data_pipeline_dag

# Check AIRFLOW_HOME is set
echo $AIRFLOW_HOME
```

### dbt connection error
```bash
cd dbt/analytics
dbt debug  # Shows connection issues
```

---

## 📚 Full Documentation

For detailed information, see:
- **README.md** - Complete project documentation
- **docs/architecture/ARCHITECTURE.md** - System architecture
- **docs/POWERBI_SETUP.md** - Power BI connection guide

---

## 💡 Tips

1. **Set up environment variables** in `.env` for production use
2. **Enable logging** by setting `LOG_LEVEL=DEBUG` in `.env`
3. **Monitor Airflow** at `http://localhost:8080`
4. **Check dbt docs** with `dbt docs serve` in dbt folder
5. **Use Docker** for isolated environment: `make docker-up`

---

## 📞 Support

- Check README.md for detailed guides
- Review logs in `logs/` directory
- Check Airflow logs in `airflow/logs/`
- See troubleshooting section in docs

---

**Happy Data Engineering!** 🎉
