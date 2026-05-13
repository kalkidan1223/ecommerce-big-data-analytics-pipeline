# Power BI Dashboard Setup Guide

## Overview

This guide explains how to connect Power BI to your DuckDB analytics database and create interactive dashboards.

## Prerequisites

1. Power BI Desktop installed ([Download](https://powerbi.microsoft.com/en-us/desktop/))
2. DuckDB ODBC Driver installed
3. Data pipeline successfully completed (DuckDB database created)
4. Access to the DuckDB database file

## Step 1: Install DuckDB ODBC Driver

### Windows

1. Download DuckDB ODBC driver:
   - Visit [DuckDB Releases](https://github.com/duckdb/duckdb/releases)
   - Download `duckdb_odbc-windows-amd64.zip`

2. Extract and install:
   ```bash
   # Extract the ZIP file
   # Run the .msi installer
   # Follow installation wizard
   ```

3. Verify installation:
   - Open ODBC Data Source Administrator
   - Check "Drivers" tab for "DuckDB Driver"

### macOS

```bash
brew install duckdb
brew install unixodbc

# Install DuckDB ODBC driver
odbc_install_driver_online
```

### Linux

```bash
# Ubuntu/Debian
sudo apt-get install odbc-duckdb unixodbc

# Or compile from source
# See: https://github.com/duckdb/duckdb/blob/main/tools/odbc/README.md
```

## Step 2: Create ODBC Data Source

### Windows

1. Open **ODBC Data Source Administrator**
   - Search for "ODBC" in Windows Start Menu
   - Click "ODBC Data Source Administrator"

2. Go to **System DSN** tab

3. Click **Add** button

4. Select **DuckDB Driver** and click **Finish**

5. Configure DSN:
   - **Data Source Name**: `DuckDB_Analytics`
   - **Database**: Full path to `data/processed/analytics.duckdb`
     ```
     C:\Users\DELL\Desktop\bigdata-analytics-project\data\processed\analytics.duckdb
     ```
   - Click **OK**

6. Verify connection

## Step 3: Connect Power BI to DuckDB

### Using Direct Query

1. Open **Power BI Desktop**

2. Click **Get Data** → **More...**

3. Search for and select **ODBC**

4. Click **Connect**

5. Select DSN: **DuckDB_Analytics**

6. Enter credentials (if required)

7. Click **OK**

8. In Navigator window:
   - Expand your ODBC connection
   - Select desired tables:
     - `orders` (staging/cleaned data)
     - `payments`
     - `items`
     - `order_summary` (aggregated)
     - `customer_metrics` (customer data)
   
   OR from dbt processed data:
     - `core.fct_orders` (Fact table)
     - `core.dim_customers` (Dimension table)

9. Click **Load** to import data

## Step 4: Create Visualizations

### Example Dashboard Pages

#### Page 1: Executive Summary
- **KPI Cards**:
  - Total Revenue (Sum of `fct_orders.total_payment`)
  - Total Orders (Count of `fct_orders.order_id`)
  - Total Customers (Count of distinct `dim_customers.customer_id`)
  - Avg Order Value (Avg of `fct_orders.total_payment`)

- **Charts**:
  - Line Chart: Revenue Trend (X: `order_year_month`, Y: `total_payment`)
  - Pie Chart: Order Status Distribution (X: `order_status`, Y: Count)

#### Page 2: Order Analytics
- **Table**: Order details with status and totals
- **Column Chart**: Orders by Status
- **Scatter Plot**: Order Value vs. Delivery Days
- **Matrix**: Revenue by Month and Status

#### Page 3: Customer Insights
- **Table**: Top customers by lifetime value
- **Pie Chart**: Customer segmentation (Active/At Risk/Inactive)
- **Column Chart**: Customer metrics comparison
- **Map** (if geographic data available): Customer distribution

#### Page 4: Payment Analysis
- **Pie Chart**: Payment method distribution
- **Column Chart**: Revenue by payment method
- **Table**: Payment summary statistics
- **Gauge**: Average installments

## Step 5: Refresh Data

### Automatic Refresh
1. Click **Settings** → **Settings** (in Power BI)
2. Go to **Data source settings**
3. Configure refresh schedule:
   - Frequency: Daily
   - Time: 3:00 AM (after pipeline completion at 2:00 AM)

### Manual Refresh
- Click **Refresh** button to update data immediately

## Data Model Best Practices

### Relationships
- Set up relationships between tables:
  - `fct_orders.customer_id` → `dim_customers.customer_id`
  - `fct_orders.order_id` ← `order_items.order_id`

### Calculated Columns
Create useful columns:

```dax
Revenue_Segment = 
SWITCH(
    TRUE(),
    [total_payment] < 100, "Under $100",
    [total_payment] < 500, "$100-$500",
    [total_payment] < 1000, "$500-$1,000",
    "Over $1,000"
)

Customer_Status_Color = 
IF([customer_status] = "Active", "Green",
   IF([customer_status] = "At Risk", "Yellow",
      "Red"))
```

### Measures
Create key metrics:

```dax
Total_Revenue = SUM(fct_orders[total_payment])

Avg_Order_Value = AVERAGE(fct_orders[total_payment])

Customer_Count = DISTINCTCOUNT(dim_customers[customer_id])

Delivery_Success_Rate = 
DIVIDE(
    CALCULATE(COUNT(fct_orders[order_id]), fct_orders[is_delivered] = 1),
    COUNT(fct_orders[order_id])
) * 100
```

## Publishing Dashboard

### To Power BI Service

1. Click **Publish** button
2. Select workspace
3. Share dashboard with stakeholders
4. Enable automatic refresh in service settings

### Sharing Reports

1. Right-click report
2. Select **Share**
3. Add email addresses
4. Grant permissions (View/Edit)

## Troubleshooting

### "Cannot connect to ODBC"
- Verify ODBC driver installation
- Check DSN configuration
- Ensure DuckDB file path is correct

### "Timeout error"
- Check network connection
- Reduce query complexity
- Try direct query instead of import

### "Data appears outdated"
- Manually refresh data
- Check automatic refresh schedule
- Verify pipeline completed successfully

### "Permission denied"
- Run Power BI as administrator
- Check DuckDB file permissions
- Ensure user has read access to database

## Example Query for Power BI

If using Direct Query, use this SQL:

```sql
SELECT
    order_id,
    customer_id,
    order_status,
    order_year_month,
    total_payment,
    num_items,
    days_to_delivery,
    is_delivered
FROM core.fct_orders
WHERE order_purchase_timestamp >= DATEADD(MONTH, -12, TODAY())
ORDER BY order_year_month DESC
```

## Performance Tips

1. **Import vs. Direct Query**:
   - Use **Import** for faster performance
   - Use **Direct Query** for real-time data

2. **Aggregations**:
   - Pre-aggregate data using `core.fct_orders`
   - Avoid aggregating 200K+ item records

3. **Filtering**:
   - Add slicers for date ranges
   - Use column-level security if needed

4. **Refresh Schedule**:
   - Avoid peak hours
   - Set to off-peak times (late night/early morning)

## Dashboard Examples

See `dashboard/powerbi/screenshots/` for example dashboard visuals.

## Additional Resources

- [Power BI Desktop Help](https://docs.microsoft.com/en-us/power-bi/desktop-what-is-desktop)
- [DuckDB ODBC Documentation](https://duckdb.org/docs/connect/odbc)
- [Power BI DAX Functions](https://docs.microsoft.com/en-us/power-bi/transform-model/dax-function-reference)
