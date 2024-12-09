# Alibaba E-commerce Analytics Repository

## Project Description
Data warehouse and analytics dashboard for Alibaba e-commerce transaction data.

## Directory Structure
```
.
├── data/                           # Data files
│   ├── raw/                       # Raw data
│   │   └── round1_ijcai_18_train_20180301.txt
│   └── processed/                 # Cleaned data
│       ├── clicked_sample.csv     
│       ├── advertising_item.csv
│       ├── user_table.csv
│       ├── context_table.csv
│       └── shop_table.csv
├── sql/                           # SQL scripts
│   ├── dataloader.sql
│   └── transform_data_for_dashboard.sql
├── src/                           # Python source code
│   ├── datacleaner.py
│   ├── fact_sales_load.py
│   └── dashboard.py
└── README.md
```

## Data Pipeline

### 1. Data Cleaning
```python
# src/datacleaner.py
- Split raw data into normalized tables
- Handle special delimiters
- Export clean CSVs
```

### 2. Database Setup 
```sql
-- sql/dataloader.sql
- Create initial tables
- Load dimensions
- Set constraints
```

### 3. Fact Table ETL
Due to the limited computational resources of the MySQL database, the fact table is generated using Python, then loaded into the database.
```python
# src/fact_sales_load.py
- Aggregate metrics
- Calculate conversions
- Export fact table
```

### 4. Star Schema
```sql
-- sql/transform_data_for_dashboard.sql
- Create dimensional model
- Time dimension handling
- Fact table structure
```

### 5. Dashboard
The dashboard in constructed using Tableau, with data source connected to MySQL.

## Database Schema

### Fact Table
- **fact_sales**
  - time_key (FK)
  - item_id (FK)
  - user_id (FK) 
  - shop_id (FK)
  - total_views
  - total_purchases
  - conversion_rate

### Dimension Tables
- **dim_time**
  - time_key (PK)
  - full_datetime
  - date_only
  - hour_of_day
  - is_peak_hour
  - is_night
  - day_of_week
  - is_weekend
  - time_segment

- **dim_product**
  - item_id (PK)
  - category_list
  - property_list
  - brand_id
  - city_id
  - price_level
  - sales_level
  - collected_level
  - pv_level

- **dim_user**
  - user_id (PK)
  - gender_id
  - age_level
  - occupation_id
  - star_level

- **dim_shop**
  - shop_id (PK)
  - review_num_level
  - review_positive_rate
  - star_level
  - score_service
  - score_delivery
  - score_description

## Pipeline
Note that file paths need to be adjusted to the local environment.
```bash
# Clean data
python src/datacleaner.py

# Generate fact table
python src/fact_sales_load.py

# Load database
mysql -u root -p < sql/dataloader.sql
mysql -u root -p < sql/transform_data_for_dashboard.sql


# Launch dashboard
streamlit run src/dashboard.py
```
