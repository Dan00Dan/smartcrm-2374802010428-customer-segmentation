# Smart CRM – Data Dictionary

## 1. Overview

The Smart CRM Data Warehouse supports customer profile management, order analysis, customer matching, data quality monitoring, and customer segmentation.

The warehouse contains two main dimension tables and one primary fact table.

## 2. Dimension Tables

### 2.1 dim_customer

Purpose: Stores customer identifiers and customer names.

| Column | Description |
|---|---|
| customer_key | Customer key used in the warehouse |
| full_name | Customer full name |

Notes:
- `customer_key` is the customer identifier.
- `UNKNOWN` represents an unresolved customer.

### 2.2 dim_period

Purpose: Stores monthly analysis periods and validation status.

| Column | Description |
|---|---|
| period_key | Period identifier in YYYYMM format |
| analysis_month | Analysis month in YYYY-MM format |
| cutoff_date | Cutoff date of the analysis period |
| status | Period processing or validation status |

Example status:
- `BLOCKED_SOURCE_VALIDATION`: Analysis is blocked because source validation has not been completed.

## 3. Fact Table

### 3.1 fact_order

Purpose: Stores order-level transactional data and customer matching information.

| Column | Description |
|---|---|
| order_business_key | Business key identifying an order |
| order_id_source | Original order identifier from the source |
| store_id | Source store identifier |
| customer_key | Matched customer key |
| customer_match_method | Method used to match the customer |
| order_date | Order date |
| analysis_month | Analysis month associated with the order |
| amount | Order amount |
| order_status | Order status from the source |
| segment_publishable | Indicates whether the order is eligible for segmentation |
| customer_id | Customer identifier from the source or matching process |

### 3.2 Customer Matching Methods

Examples of customer matching methods:

| Method | Description |
|---|---|
| PHONE_UNIQUE | Customer matched using a unique phone number |
| PHONE_NAME_DUPLICATE_CANDIDATE | Phone and name matching produced duplicate candidates |
| UNKNOWN | Customer could not be resolved |

## 4. Data Quality Tables

### 4.1 data_quality_issues

Purpose: Records orders with unresolved customer information or other data quality issues.

| Column | Description |
|---|---|
| order_business_key | Business key of the affected order |
| order_id_source | Original order identifier |
| store_id | Source store identifier |
| issue_code | Code describing the data quality issue |

Example:
- `CUSTOMER_NOT_RESOLVED`: Customer could not be identified.

### 4.2 customer_duplicate_candidates

Purpose: Stores potential duplicate customer records for review.

| Column | Description |
|---|---|
| phone_norm | Normalized phone number |
| name_norm | Normalized customer name |
| candidate_count | Number of candidate records |
| representative_record_id | Representative record identifier |
| candidate_record_ids | List of candidate record identifiers |
| email_distinct_count | Number of distinct email values |
| address_distinct_count | Number of distinct address values |

This table supports duplicate detection and manual customer identity review.

## 5. Relationships

- `fact_order.customer_key` references `dim_customer.customer_key`.
- `fact_order.analysis_month` corresponds to `dim_period.analysis_month`.
- `data_quality_issues.order_business_key` identifies affected orders in `fact_order`.
- `customer_duplicate_candidates` supports customer duplicate investigation.

## 6. Data Quality and Segmentation Rules

- Orders with unresolved customers are assigned the `UNKNOWN` customer key.
- Orders with unresolved customer identity are recorded in `data_quality_issues`.
- Orders with `segment_publishable = False` are excluded from segmentation calculations.
- Analysis periods with `BLOCKED_SOURCE_VALIDATION` status must not be treated as validated segmentation periods.

## 7. Notes

- `fact_order.csv` is the primary fact table used in this documentation.
- `fact_orders.csv` currently has the same column structure and sample records as `fact_order.csv`. Its role should be confirmed before using it as a separate table.
- Data types and constraints should be verified against the actual ETL implementation before final database schema documentation.