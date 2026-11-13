# Smart CRM – Data Dictionary

**Version:** 1.2  
**Last Updated:** 13 November 2026  
**Project:** Smart CRM – Customer Segmentation  
**Track:** Data Analyst – L1 Customer Profile & Segmentation

## 1. Overview

The Smart CRM Data Warehouse supports customer profile management, order analysis, customer matching, data quality monitoring, and customer segmentation.

The documented warehouse consists of the following logical tables:

- `dim_customer`: Customer dimension.
- `dim_period`: Analysis period dimension.
- `fact_order`: Order transaction fact table.
- `data_quality_issues`: Data quality issue records.
- `customer_duplicate_candidates`: Potential duplicate customer records.

This document describes the logical structure, field definitions, relationships, and business rules used by the Smart CRM data processing pipeline.

## 2. Dimension Tables

### 2.1 dim_customer

**Purpose:** Stores customer identifiers and customer names used in customer analysis.

| Column | Description | Data Type | Key |
|---|---|---|---|
| customer_key | Customer identifier used in the warehouse | String | Logical PK |
| full_name | Customer full name | String | |

**Business Rules:**
- `customer_key` identifies a customer record in the warehouse.
- `UNKNOWN` represents an unresolved customer identity.
- Customer identity resolution is performed during data processing.

### 2.2 dim_period

**Purpose:** Stores monthly analysis periods and their processing or validation status.

| Column | Description | Data Type | Key |
|---|---|---|---|
| period_key | Period identifier in YYYYMM format | Integer | Logical PK |
| analysis_month | Analysis month in YYYY-MM format | String | |
| cutoff_date | Cutoff date for the analysis period | Date | |
| status | Period processing or validation status | String | |

**Business Rules:**
- Each analysis period is represented by a monthly identifier.
- `BLOCKED_SOURCE_VALIDATION` indicates that source validation has not been completed.
- A blocked period must not be treated as a validated segmentation result.

## 3. Fact Table

### 3.1 fact_order

**Purpose:** Stores order-level transactional data and customer matching information.

| Column | Description | Data Type | Key |
|---|---|---|---|
| order_business_key | Business key identifying an order | String | Logical PK |
| order_id_source | Original order identifier from the source | String | |
| store_id | Source store identifier | String | |
| customer_key | Matched customer key | String | Logical FK |
| customer_match_method | Customer matching method | String | |
| order_date | Order transaction date | Date | |
| analysis_month | Analysis month associated with the order | String | |
| amount | Order amount | Numeric | |
| order_status | Order status from the source | String | |
| segment_publishable | Indicates whether the order is eligible for segmentation | Boolean | |
| customer_id | Customer identifier from the source or matching process | String | |

**Business Rules:**
- `order_business_key` identifies an order within the warehouse.
- `customer_key` references `dim_customer.customer_key`.
- Orders with unresolved customer identity are assigned the `UNKNOWN` customer key.
- Orders with `segment_publishable = False` are excluded from segmentation calculations.
- Invalid orders are rejected during data processing and recorded with rejection reasons.

## 4. Customer Matching Methods

| Method | Description |
|---|---|
| PHONE_UNIQUE | Customer matched using a unique normalized phone number |
| PHONE_NAME_DUPLICATE_CANDIDATE | Phone and name matching produced potential duplicate candidates |
| UNKNOWN | Customer identity could not be resolved |

These methods support customer identity resolution and data quality monitoring.

## 5. Data Quality Tables

### 5.1 data_quality_issues

**Purpose:** Records orders with unresolved customer information or other data quality issues.

| Column | Description | Data Type | Key |
|---|---|---|---|
| order_business_key | Business key of the affected order | String | Logical reference |
| order_id_source | Original order identifier | String | |
| store_id | Source store identifier | String | |
| issue_code | Code describing the data quality issue | String | |

**Example issue code:**

- `CUSTOMER_NOT_RESOLVED`: Customer identity could not be identified.

### 5.2 customer_duplicate_candidates

**Purpose:** Stores potential duplicate customer records for investigation and manual review.

| Column | Description | Data Type | Key |
|---|---|---|---|
| phone_norm | Normalized phone number | String | |
| name_norm | Normalized customer name | String | |
| candidate_count | Number of candidate records | Integer | |
| representative_record_id | Representative record identifier | String | |
| candidate_record_ids | List of candidate record identifiers | String/List | |
| email_distinct_count | Number of distinct email values | Integer | |
| address_distinct_count | Number of distinct address values | Integer | |

**Business Rules:**
- Candidate records are generated based on normalized phone and name information.
- Duplicate candidates are not automatically merged.
- Manual review is required before making customer identity decisions.

## 6. Relationships

| Relationship | Description |
|---|---|
| fact_order.customer_key → dim_customer.customer_key | Associates each order with a warehouse customer |
| fact_order.analysis_month → dim_period.analysis_month | Associates each order with its analysis period |
| data_quality_issues.order_business_key → fact_order.order_business_key | Identifies the order associated with a data quality issue |
| customer_duplicate_candidates | Supports duplicate customer investigation and review |

These relationships describe the logical data model. Physical database constraints should be verified against the actual warehouse implementation.

## 7. Data Quality and Segmentation Rules

- Unresolved customer identities are represented using `UNKNOWN`.
- Customer identity issues are recorded in `data_quality_issues`.
- Orders with `segment_publishable = False` are excluded from segmentation calculations.
- Orders that fail validation are rejected with corresponding rejection reasons.
- Analysis periods with `BLOCKED_SOURCE_VALIDATION` status must not be treated as validated segmentation periods.
- Customer matching and duplicate candidate detection support data quality review before segmentation publication.

## 8. Data Types and Constraints

The data types in this document represent the logical data model.

Actual CSV data types may differ because of pandas inference, missing values, or ETL transformations.

| Constraint | Description |
|---|---|
| Logical Primary Key | Identifies a record uniquely within its logical table |
| Logical Foreign Key | Represents a relationship between warehouse tables |
| Nullable Fields | May contain missing values depending on source data and ETL processing |
| Data Validation | Applied during extraction, normalization, and warehouse loading |
| Referential Integrity | Logical relationships are documented; physical constraints require implementation verification |

## 9. Table and File Naming Notes

- `fact_order` is the logical order fact table documented in this specification.
- `fact_order.csv` and `fact_orders.csv` may exist as separate warehouse files.
- Their physical roles and equivalence must be verified against the ETL implementation before treating them as independent logical tables.
- The logical model does not automatically imply that every documented relationship is enforced by a database constraint.

## 10. Verification Status

This Data Dictionary describes the logical warehouse structure based on the project documentation and ETL design.

The following items require verification against the actual warehouse implementation:

- Exact physical data types.
- Primary key uniqueness.
- Foreign key enforcement.
- Nullable field constraints.
- The role and equivalence of `fact_order.csv` and `fact_orders.csv`.

The Data Dictionary should be updated whenever the warehouse schema or ETL implementation changes.
