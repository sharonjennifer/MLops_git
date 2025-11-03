# MLOps Lab 1 - CI/CD Pipeline with Data Quality Analyzer

[![Testing with Pytest](https://github.com/sharonjennifer/MLops_git/actions/workflows/github_lab1_pytest_action.yml/badge.svg)](https://github.com/sharonjennifer/MLops_git/actions)
[![Python Unittests](https://github.com/sharonjennifer/MLops_git/actions/workflows/github_lab2_unittest_action.yml/badge.svg)](https://github.com/sharonjennifer/MLops_git/actions)
[![Data Quality Tests](https://github.com/sharonjennifer/MLops_git/actions/workflows/data_quality_tests.yml/badge.svg)](https://github.com/sharonjennifer/MLops_git/actions)

## Overview

This project demonstrates a complete MLOps CI/CD pipeline with automated testing, version control, and a practical Data Quality Analyzer tool. It showcases key MLOps practices including environment management, automated testing with pytest and unittest, and continuous integration using GitHub Actions.

## Project Components

### 1. Calculator Module
Simple arithmetic operations demonstrating basic Python testing concepts.

**Functions:**
- `fun1(x, y)` - Addition
- `fun2(x, y)` - Subtraction
- `fun3(x, y)` - Multiplication
- `fun4(x, y)` - Combined operations

### 2. Data Quality Analyzer
A comprehensive tool for analyzing CSV data quality, detecting issues, and generating detailed reports. This is the primary focus of the project.

**Core Features:**
- Missing value detection with counts and percentages
- Duplicate row identification
- Outlier detection using IQR and Z-score methods
- Statistical analysis (mean, median, std, min, max)
- Data type validation
- Overall quality score calculation (0-100)
- JSON report generation
- Multi-encoding support for international datasets

## Project Structure
```
MLops_git/
├── .github/
│   └── workflows/
│       ├── github_lab1_pytest_action.yml    # Pytest workflow
│       ├── github_lab2_unittest_action.yml  # Unittest workflow
│       └── data_quality_tests.yml           # Data analyzer tests
├── data/
│   ├── raw/
│   │   ├── sample_clean.csv                 # Clean test dataset
│   │   ├── sample_with_issues.csv           # Dataset with quality issues
│   │   └── ecommerce.csv                    # Real-world data (gitignored)
│   └── processed/
├── reports/                                  # Generated quality reports
│   ├── .gitkeep
│   └── ecommerce_report.json
├── src/
│   ├── __init__.py
│   ├── calculator.py                        # Basic calculator functions
│   └── data_analyzer.py                     # Data quality analyzer
├── test/
│   ├── __init__.py
│   ├── test_pytest.py                       # Calculator pytest tests
│   ├── test_unittest.py                     # Calculator unittest tests
│   └── test_data_analyzer.py                # Data analyzer tests (21 tests)
├── .gitignore
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git

### Installation

1. Clone the repository
```bash
   git clone https://github.com/sharonjennifer/MLops_git.git
   cd MLops_git
```

2. Create and activate virtual environment
```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Mac/Linux
   source venv/bin/activate
```

3. Install dependencies
```bash
   pip install -r requirements.txt
```

## Usage

### Data Quality Analyzer

Analyze CSV files for quality issues:
```bash
python src/data_analyzer.py <path_to_csv> [output_json_path]
```

**Examples:**
```bash
# Analyze clean data
python src/data_analyzer.py data/raw/sample_clean.csv reports/clean_report.json

# Analyze data with issues
python src/data_analyzer.py data/raw/sample_with_issues.csv reports/issues_report.json
```

**Sample Console Output:**
```
==================================================
DATA QUALITY REPORT
==================================================
Total Rows: 12
Total Columns: 6
Missing Values: 4 columns affected
Duplicates: 1 rows
Outliers: 2 columns with outliers
Quality Score: 95.28/100

Full report saved to: reports/issues_report.json
```

### Using as a Python Module
```python
from src.data_analyzer import generate_quality_report, load_data, detect_outliers

# Generate full report
report = generate_quality_report('data/raw/sample_clean.csv')
print(f"Quality Score: {report['quality_score']}")

# Use individual functions
df = load_data('data/raw/sample_clean.csv')
outliers = detect_outliers(df, 'age')
```

## Real-World Analysis Results

### E-commerce Dataset Analysis

The analyzer was tested on a real e-commerce dataset containing 541,909 transactions with 8 columns.

**Quality Metrics:**
- **Total Records:** 541,909 transactions
- **Total Columns:** 8 (InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country)
- **Overall Quality Score:** 98.45/100

**Issues Detected:**

| Issue Type | Details |
|------------|---------|
| **Missing Values** | 2 columns affected |
| - CustomerID | 135,080 missing (24.93%) |
| - Description | 1,454 missing (0.27%) |
| **Duplicate Records** | 5,268 duplicate transactions |
| **Outliers** | 2 columns affected |
| - Quantity | 58,619 outliers detected |
| - UnitPrice | 39,627 outliers detected |

**Interpretation:** Despite significant missing CustomerID data and numerous outliers in pricing and quantity, the dataset maintains a high quality score of 98.45/100, indicating it is usable with appropriate preprocessing.

### About the E-commerce Dataset

**Dataset Details:**
- **Source:** Online Retail Dataset
- **Size:** 541,909 transactions, 8 columns, 44.5 MB
- **Columns:** InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country
- **Location:** Not included in repository (exceeds GitHub file size recommendations)

**Why Not Included:**
Following MLOps best practices, large datasets (>10 MB) are excluded from version control to:
- Keep repository lightweight and cloneable
- Avoid GitHub storage limitations
- Follow industry standards for data management
- Enable faster CI/CD pipeline execution

**To Replicate Analysis:**
Users can download similar e-commerce datasets from:
- Kaggle: Online Retail datasets
- UCI Machine Learning Repository
- Public data repositories

The complete analysis results are preserved in `reports/ecommerce_report.json`, demonstrating the tool's effectiveness on production-scale data.

### Sample Datasets Included

Two small sample datasets are provided in `data/raw/` for testing and demonstration:
- `sample_clean.csv` - 10 rows with perfect data quality (100/100 score)
- `sample_with_issues.csv` - 12 rows with intentional quality issues (95.28/100 score)

## Testing

The project includes comprehensive test coverage with both pytest and unittest frameworks.

**Run all tests:**
```bash
# Pytest tests
pytest test/test_pytest.py -v
pytest test/test_data_analyzer.py -v

# Unittest tests
python -m unittest test.test_unittest -v
```

**Test Coverage:**
- Calculator: 8 tests (pytest + unittest)
- Data Analyzer: 21 tests covering all functions
- **Total: 29 automated tests with 100% pass rate**

## CI/CD Pipeline

GitHub Actions automatically runs all tests on every push to the main branch. Three workflows are configured:

1. **Pytest Workflow** - Tests calculator module with pytest
2. **Unittest Workflow** - Tests calculator module with unittest  
3. **Data Quality Tests** - Tests data analyzer with 21 test cases and runs analysis on sample data

All workflows must pass before code changes are accepted, ensuring code quality and preventing regressions.

## Data Quality Metrics

The analyzer calculates the following metrics:

| Metric | Description |
|--------|-------------|
| Missing Values | Count and percentage of missing values per column |
| Duplicates | Number of duplicate rows with indices |
| Outliers | Extreme values using IQR or Z-score methods |
| Statistics | Mean, median, std, min, max for numeric columns |
| Data Types | Column data types validation |
| Quality Score | Overall score (0-100) based on data completeness and consistency |

## Technologies Used

- **Python 3.11** - Primary programming language
- **pandas** - Data manipulation and analysis
- **numpy** - Numerical operations
- **pytest** - Testing framework
- **unittest** - Built-in testing framework
- **GitHub Actions** - CI/CD automation

## Key Features

- Automated testing with 29 test cases
- Continuous Integration with GitHub Actions
- Comprehensive data quality analysis on production-scale datasets
- JSON report generation
- Multiple outlier detection methods (IQR, Z-score)
- Automatic encoding detection for international data
- Clean, documented, and maintainable code
- Production-ready error handling


## Repository Information

**Author:** Sharon Jennifer Justin Devaraj
**Course:** MLOps (IE-7374)  
**Repository:** [github.com/sharonjennifer/MLops_git](https://github.com/sharonjennifer/MLops_git)

## License

This project is part of academic coursework for MLOps (IE-7374).