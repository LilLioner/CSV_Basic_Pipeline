# Data Cleaning Pipeline for CSV Files (Actually on Beta - with some bugs)

## Overview

This project implements a data cleaning pipeline for CSV files, simulating a real-world data engineering scenario where data originates from heterogeneous sources with inconsistent formats.

The pipeline standardizes, validates, and cleans raw data, producing a structured and reliable dataset suitable for downstream analysis.

This project was developed for learning purposes, with a focus on applying practical data engineering concepts such as data validation, schema enforcement, and transformation logic.

---

## Objective

The main objective of this pipeline is to:

- Standardize input data with varying column names and formats
- Validate required fields and data integrity
- Clean inconsistent and invalid records
- Output a structured dataset following a predefined schema

---

## Expected Data Schema

The pipeline processes sales-related data with the following schema:

| Column          | Description                     |
|----------------|---------------------------------|
| id             | Unique transaction identifier   |
| cliente        | Customer name                   |
| valor_produto  | Unit price of the product       |
| quantidade     | Quantity purchased              |
| cidade         | Location of the transaction     |
| produto        | Product name                    |

---

## Business Rules

### Column Standardization

- All column names are normalized to lowercase
- Spaces are replaced with underscores
- Equivalent column names are mapped to a standard schema

Examples:

- `preco`, `price` → `valor_produto`
- `qtd`, `quantity` → `quantidade`

---

### Required Columns Validation

The following columns are mandatory:

- `id`
- `valor_produto`
- `quantidade`

If any of these columns are missing, the file is rejected and not processed.

---

### Optional Columns Handling

Optional columns:

- `cliente`
- `cidade`
- `produto`

Rules:

- Missing columns are created
- Null or missing values are filled with default values:

| Column   | Default Value     |
|----------|-------------------|
| cliente  | desconhecido      |
| cidade   | desconhecido      |
| produto  | nao_informado     |

---

### Data Type Enforcement

- Numeric columns (`id`, `quantidade`, `valor_produto`) are converted to numeric types
- Invalid values are coerced to null (`NaN`)

---

### Invalid Data Filtering

Records are removed if:

- `quantidade <= 0`
- `valor_produto <= 0`
- `valor_produto > 10000` (treated as an outlier)

---

### Null Handling

- Rows with null values in required columns are removed

---

### Duplicate Handling

- Duplicate records are removed based on the `id` column
- The first occurrence is retained

---

### Text Normalization

Text fields are:

- Trimmed (whitespace removed)
- Converted to lowercase

---

### Derived Column

A new column is created:

- `valor_total = valor_produto * quantidade`

---

### Data Ordering

- The final dataset is sorted by `valor_total` in descending order

---

### Output

- Processed files are saved in:
data/processed/

- Output file naming convention:
<original_filename>_limpo.csv

---

### Error Handling

- Errors in individual files do not interrupt the pipeline
- Failed files are logged and skipped
- Error messages are displayed in the console

---

## Project Structure

data/
raw/ # Input files
processed/ # Cleaned output files

---

## Future Improvements

- Structured logging
- Processing reports (metrics and statistics)
- Command-line interface (CLI)
- Integration with databases or data warehouses
- Automated testing

---

## Status

This project is currently under development and should be considered a beta version.