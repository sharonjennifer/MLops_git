# \# MLOps Lab 1 - CI/CD Pipeline with Data Quality Analyzer

# 

# \[!\[Testing with Pytest](https://github.com/sharonjennifer/MLops\_git/actions/workflows/github\_lab1\_pytest\_action.yml/badge.svg)](https://github.com/sharonjennifer/MLops\_git/actions)

# \[!\[Python Unittests](https://github.com/sharonjennifer/MLops\_git/actions/workflows/github\_lab2\_unittest\_action.yml/badge.svg)](https://github.com/sharonjennifer/MLops\_git/actions)

# \[!\[Data Quality Tests](https://github.com/sharonjennifer/MLops\_git/actions/workflows/data\_quality\_tests.yml/badge.svg)](https://github.com/sharonjennifer/MLops\_git/actions)

# 

# \## Overview

# 

# This project demonstrates a complete \*\*MLOps CI/CD pipeline\*\* with automated testing, version control, and a practical \*\*Data Quality Analyzer\*\* tool. The project showcases key MLOps practices including environment management, automated testing with pytest and unittest, and continuous integration using GitHub Actions.

# 

# \## 🎯 Project Components

# 

# \### 1. Calculator Module (Basic Example)

# \- Simple arithmetic operations (add, subtract, multiply)

# \- Demonstrates basic Python testing concepts

# \- Located in `src/calculator.py`

# 

# \### 2. Data Quality Analyzer (Main Project)

# A comprehensive tool for analyzing CSV data quality, detecting issues, and generating detailed reports.

# 

# \*\*Features:\*\*

# \- ✅ Missing value detection with counts and percentages

# \- ✅ Duplicate row identification

# \- ✅ Outlier detection using IQR and Z-score methods

# \- ✅ Statistical analysis (mean, median, std, min, max)

# \- ✅ Data type validation

# \- ✅ Overall quality score calculation (0-100)

# \- ✅ JSON report generation

# 

# \## 📁 Project Structure

# ```

# MLops\_git/

# ├── .github/

# │   └── workflows/

# │       ├── github\_lab1\_pytest\_action.yml    # Pytest workflow

# │       ├── github\_lab2\_unittest\_action.yml  # Unittest workflow

# │       └── data\_quality\_tests.yml           # Data analyzer tests

# ├── data/

# │   ├── raw/

# │   │   ├── sample\_clean.csv                 # Clean test dataset

# │   │   └── sample\_with\_issues.csv           # Dataset with quality issues

# │   └── processed/

# ├── reports/                                  # Generated quality reports

# │   └── .gitkeep

# ├── src/

# │   ├── \_\_init\_\_.py

# │   ├── calculator.py                        # Basic calculator functions

# │   └── data\_analyzer.py                     # Data quality analyzer

# ├── test/

# │   ├── \_\_init\_\_.py

# │   ├── test\_pytest.py                       # Calculator pytest tests

# │   ├── test\_unittest.py                     # Calculator unittest tests

# │   └── test\_data\_analyzer.py                # Data analyzer tests (21 tests)

# ├── .gitignore

# ├── requirements.txt

# └── README.md

# ```

# 

# \## 🚀 Getting Started

# 

# \### Prerequisites

# \- Python 3.8+

# \- pip

# 

# \### Installation

# 

# 1\. \*\*Clone the repository\*\*

# ```bash

# &nbsp;  git clone https://github.com/sharonjennifer/MLops\_git.git

# &nbsp;  cd MLops\_git

# ```

# 

# 2\. \*\*Create virtual environment\*\*

# ```bash

# &nbsp;  python -m venv venv

# &nbsp;  

# &nbsp;  # On Windows

# &nbsp;  venv\\Scripts\\activate

# &nbsp;  

# &nbsp;  # On Mac/Linux

# &nbsp;  source venv/bin/activate

# ```

# 

# 3\. \*\*Install dependencies\*\*

# ```bash

# &nbsp;  pip install -r requirements.txt

# ```

# 

# \## 💻 Usage

# 

# \### Data Quality Analyzer

# 

# \*\*Analyze a CSV file:\*\*

# ```bash

# python src/data\_analyzer.py <path\_to\_csv> \[output\_json\_path]

# ```

# 

# \*\*Examples:\*\*

# ```bash

# \# Analyze clean data

# python src/data\_analyzer.py data/raw/sample\_clean.csv reports/clean\_report.json

# 

# \# Analyze data with issues

# python src/data\_analyzer.py data/raw/sample\_with\_issues.csv reports/issues\_report.json

# ```

# 

# \*\*Sample Output:\*\*

# ```

# ==================================================

# DATA QUALITY REPORT

# ==================================================

# Total Rows: 12

# Total Columns: 6

# Missing Values: 4 columns affected

# Duplicates: 1 rows

# Outliers: 2 columns with outliers

# Quality Score: 95.28/100

# 

# Full report saved to: reports/issues\_report.json

# ```

# 

# \### Using as a Python Module

# ```python

# from src.data\_analyzer import generate\_quality\_report, load\_data, detect\_outliers

# 

# \# Generate full report

# report = generate\_quality\_report('data/raw/sample\_clean.csv')

# print(f"Quality Score: {report\['quality\_score']}")

# 

# \# Use individual functions

# df = load\_data('data/raw/sample\_clean.csv')

# outliers = detect\_outliers(df, 'age')

# print(f"Outliers in age column: {outliers}")

# ```

# 

# \## 🧪 Testing

# 

# The project includes comprehensive test coverage with both pytest and unittest frameworks.

# 

# \*\*Run all tests:\*\*

# ```bash

# \# Run pytest tests

# pytest test/test\_pytest.py -v

# pytest test/test\_data\_analyzer.py -v

# 

# \# Run unittest tests

# python -m unittest test.test\_unittest -v

# ```

# 

# \*\*Test Coverage:\*\*

# \- Calculator: 8 tests (pytest + unittest)

# \- Data Analyzer: 21 tests covering all functions

# \- \*\*Total: 29 automated tests\*\*

# 

# \## 🔄 CI/CD Pipeline

# 

# GitHub Actions automatically runs all tests on every push to the main branch.

# 

# \*\*Workflows:\*\*

# 1\. \*\*Pytest Workflow\*\* - Tests calculator module with pytest

# 2\. \*\*Unittest Workflow\*\* - Tests calculator module with unittest

# 3\. \*\*Data Quality Tests\*\* - Tests data analyzer with 21 test cases

# 

# All workflows must pass before code is merged, ensuring code quality and preventing regressions.

# 

# \## 📊 Data Quality Metrics

# 

# The analyzer calculates the following metrics:

# 

# | Metric | Description |

# |--------|-------------|

# | \*\*Missing Values\*\* | Count and percentage of missing values per column |

# | \*\*Duplicates\*\* | Number of duplicate rows and their indices |

# | \*\*Outliers\*\* | Extreme values using IQR or Z-score methods |

# | \*\*Statistics\*\* | Mean, median, std, min, max for numeric columns |

# | \*\*Data Types\*\* | Column data types validation |

# | \*\*Quality Score\*\* | Overall score (0-100) based on data quality |

# 

# \## 🛠️ Technologies Used

# 

# \- \*\*Python 3.11\*\* - Programming language

# \- \*\*pandas\*\* - Data manipulation and analysis

# \- \*\*numpy\*\* - Numerical operations

# \- \*\*pytest\*\* - Testing framework

# \- \*\*unittest\*\* - Built-in testing framework

# \- \*\*GitHub Actions\*\* - CI/CD automation

# 

# \## 📈 Key Features

# 

# \- ✅ Automated testing with 100% pass rate

# \- ✅ Continuous Integration with GitHub Actions

# \- ✅ Comprehensive data quality analysis

# \- ✅ JSON report generation

# \- ✅ Multiple outlier detection methods

# \- ✅ Clean, documented, and maintainable code

# \- ✅ Production-ready error handling

# 

# \## 🎓 Learning Outcomes

# 

# This project demonstrates:

# \- Virtual environment management

# \- Version control with Git

# \- Test-driven development (TDD)

# \- CI/CD pipeline implementation

# \- Data quality validation techniques

# \- MLOps best practices

# \- Clean code principles

# 

# \## 📝 Future Enhancements

# 

# \- \[ ] Add HTML report generation with visualizations

# \- \[ ] Implement data profiling dashboard

# \- \[ ] Add more outlier detection methods

# \- \[ ] Support for multiple file formats (Excel, JSON)

# \- \[ ] Add data validation rules engine

# \- \[ ] Integration with data versioning tools (DVC)

# 

# \## 👤 Author

# 

# \*\*Sharon Jennifer\*\*

# \- GitHub: \[@sharonjennifer](https://github.com/sharonjennifer)

# 

# \## 📄 License

# 

# This project is part of MLOps coursework (IE-7374).

# 

# ---

