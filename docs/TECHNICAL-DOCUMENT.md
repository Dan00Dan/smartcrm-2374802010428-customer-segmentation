# TECHNICAL DOCUMENT – SMART CRM

**Project:** Smart CRM – L1 Customer Profile and Segmentation  
**Student:** Trần Thị Như Quỳnh  
**Student ID:** 2374802010428  
**Track:** Data Analyst  
**Version:** 1.0

## 1. System Overview

Smart CRM is a data-driven customer analysis system designed to support Marketing employees in customer profiling, customer segmentation, order analysis, and data quality monitoring.

The system processes customer and order data through an ETL pipeline, stores standardized data in a Data Warehouse, and provides analytical information through a Streamlit dashboard.

The system focuses on improving customer data consistency and supporting customer segmentation based on business rules QT-12.

## 2. System Architecture

The system consists of the following main components:

| Component | Technology | Responsibility |
|---|---|---|
| User Interface | Streamlit | Display dashboard, analysis results, and data quality information |
| Data Processing | Python, Pandas | Data cleaning, normalization, validation, and transformation |
| Data Storage | Data Warehouse | Store standardized customer and order data |
| ETL Pipeline | Python | Extract, transform, validate, and load data |
| Containerization | Docker, Docker Compose | Build and run the application environment |
| Testing | pytest | Validate ETL functions and business logic |

The architecture separates data processing, storage, and presentation to improve maintainability and reproducibility.

## 3. Data Pipeline

The Smart CRM data pipeline follows these stages:

### 3.1 Data Extraction

Customer and order data are collected from the available source datasets and loaded into the processing environment.

### 3.2 Data Cleaning and Transformation

The ETL process performs:

- Standardization of date and monetary values.
- Validation of required columns.
- Detection of duplicate business keys.
- Identification of invalid or incomplete records.
- Customer identity matching.
- Classification of valid and rejected orders.

### 3.3 Customer Matching

Customer matching uses normalized identifiers and available customer information.

Matching methods include:

- `PHONE_UNIQUE`
- `PHONE_NAME_DUPLICATE_CANDIDATE`
- `UNKNOWN`

Unresolved customer records are assigned the `UNKNOWN` key and recorded for data quality monitoring.

### 3.4 Data Warehouse Loading

The ETL pipeline loads standardized data into the Warehouse.

The main tables include:

- `dim_customer`
- `dim_period`
- `fact_order`
- `data_quality_issues`
- `customer_duplicate_candidates`

### 3.5 Data Quality Monitoring

The system records unresolved customer identities, potential duplicates, and other data quality issues.

Orders that cannot be validated for customer identity are excluded from customer segmentation calculations.

### 3.6 Segmentation and Dashboard

The system applies QT-12 business rules to eligible customer data and provides analytical information through the Streamlit dashboard.

Segmentation publication is controlled by source validation status. When validation is incomplete, the analysis period is marked `BLOCKED_SOURCE_VALIDATION`.

## 4. Business Logic

### 4.1 Customer Segmentation – QT-12

Customer segments are assigned according to purchase behavior:

| Segment | Business Rule |
|---|---|
| VIP | Spending ≥ 30 million VND or ≥ 8 orders in 12 months |
| Regular | Spending ≥ 10 million VND or ≥ 3 orders in 12 months |
| New | Exactly one valid completed order within the last 90 days |
| Dormant | Customers who do not satisfy the previous segment conditions |

Priority order:

**VIP → Regular → New → Dormant**

The segmentation function is designed to avoid modifying the original input DataFrame.

### 4.2 Data Validation

The system distinguishes between valid and rejected orders.

Invalid records are retained in the data quality processing results instead of silently disappearing.

### 4.3 Source Validation Control

The segmentation process must not be treated as validated when the source order completion status or customer identity cannot be sufficiently verified.

The current publication status is:

`BLOCKED_SOURCE_VALIDATION`

This status indicates that source validation requirements remain incomplete.

## 5. Business Impact

Smart CRM provides the following benefits:

- Supports Marketing employees in understanding customer purchase behavior.
- Improves visibility into customer data quality.
- Helps identify potential duplicate customer records.
- Provides structured information for customer segmentation.
- Supports monthly analysis and comparison.
- Improves transparency through validation and data quality reporting.

The system is intended to support analytical decision-making rather than automatically execute marketing campaigns.

## 6. Limitations

Current system limitations include:

- Some customer identities remain unresolved.
- Potential duplicate customer records require further review.
- Source order completion status cannot be fully verified.
- Customer segmentation publication is currently blocked by source validation.
- Customer identity matching still requires additional source validation.
- The system is a prototype and is not yet ready for production use with real customer data without additional security and access control measures.

## 7. Data Dictionary

The following tables define the primary Warehouse structures.

| Table | Description |
|---|---|
| `dim_customer` | Customer identifiers and customer names |
| `dim_period` | Analysis periods and validation status |
| `fact_order` | Order-level transactional data and customer matching information |
| `data_quality_issues` | Orders with unresolved customer information or other quality issues |
| `customer_duplicate_candidates` | Potential duplicate customer records for investigation |

### 7.1 Key Relationships

- `fact_order.customer_key` references `dim_customer.customer_key`.
- `fact_order.analysis_month` corresponds to `dim_period.analysis_month`.
- `data_quality_issues.order_business_key` identifies affected orders in `fact_order`.
- `customer_duplicate_candidates` supports duplicate customer investigation.

Detailed column definitions are provided in `docs/DATA-DICTIONARY.md`.

## 8. Technical Conclusion

Smart CRM implements a data processing and analytical workflow for customer profiling and segmentation.

The ETL pipeline, Data Warehouse, data quality monitoring, and dashboard provide the technical foundation for customer analysis.

The system has passed its documented automated tests. However, segmentation publication remains blocked until the outstanding source validation requirements are resolved.

