import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
import json


def load_data(file_path: str) -> pd.DataFrame:
    """
    Load CSV file into a pandas DataFrame with automatic encoding detection.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        pd.DataFrame: Loaded data
    """
    encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
    
    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            return df
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            if encoding == encodings[-1]:  # Last encoding attempt
                raise Exception(f"Error loading file: {str(e)}")
            continue
    
    raise Exception(f"Could not decode file with any supported encoding")

def check_missing_values(df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """
    Check for missing values in the DataFrame.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Dictionary with missing value counts and percentages per column
    """
    missing_info = {}
    total_rows = len(df)
    
    for column in df.columns:
        missing_count = df[column].isna().sum()
        if missing_count > 0:
            missing_info[column] = {
                'count': int(missing_count),
                'percentage': round((missing_count / total_rows) * 100, 2)
            }
    
    return missing_info


def detect_duplicates(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Detect duplicate rows in the DataFrame.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Dictionary with duplicate count and indices
    """
    duplicates = df.duplicated()
    duplicate_count = duplicates.sum()
    duplicate_indices = df[duplicates].index.tolist()
    
    return {
        'count': int(duplicate_count),
        'indices': duplicate_indices
    }


def detect_outliers(df: pd.DataFrame, column: str, method: str = 'iqr') -> List[Any]:
    """
    Detect outliers in a numeric column using IQR method.
    
    Args:
        df: Input DataFrame
        column: Column name to check
        method: Method for outlier detection ('iqr' or 'zscore')
        
    Returns:
        List of outlier values
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame")
    
    # Select only numeric columns
    if not pd.api.types.is_numeric_dtype(df[column]):
        return []
    
    # Remove NaN values
    data = df[column].dropna()
    
    if method == 'iqr':
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = data[(data < lower_bound) | (data > upper_bound)].tolist()
    elif method == 'zscore':
        mean = data.mean()
        std = data.std()
        z_scores = np.abs((data - mean) / std)
        outliers = data[z_scores > 3].tolist()
    else:
        raise ValueError("Method must be 'iqr' or 'zscore'")
    
    return outliers


def calculate_statistics(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    """
    Calculate basic statistics for numeric columns.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Dictionary with statistics per numeric column
    """
    stats = {}
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    
    for column in numeric_columns:
        data = df[column].dropna()
        if len(data) > 0:
            stats[column] = {
                'mean': round(float(data.mean()), 2),
                'median': round(float(data.median()), 2),
                'std': round(float(data.std()), 2),
                'min': round(float(data.min()), 2),
                'max': round(float(data.max()), 2)
            }
    
    return stats


def check_data_types(df: pd.DataFrame) -> Dict[str, str]:
    """
    Get data types of all columns.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Dictionary mapping column names to data types
    """
    return {col: str(dtype) for col, dtype in df.dtypes.items()}


def calculate_quality_score(df: pd.DataFrame, missing_info: Dict, duplicate_count: int) -> float:
    """
    Calculate an overall data quality score (0-100).
    
    Args:
        df: Input DataFrame
        missing_info: Missing values information
        duplicate_count: Number of duplicate rows
        
    Returns:
        Quality score between 0 and 100
    """
    total_cells = df.shape[0] * df.shape[1]
    total_missing = sum(info['count'] for info in missing_info.values())
    
    # Deduct points for missing values and duplicates
    missing_penalty = (total_missing / total_cells) * 40  # Up to 40 points
    duplicate_penalty = min((duplicate_count / len(df)) * 30, 30)  # Up to 30 points
    
    score = 100 - missing_penalty - duplicate_penalty
    return round(max(score, 0), 2)


def generate_quality_report(file_path: str, output_path: str = None) -> Dict[str, Any]:
    """
    Generate a comprehensive data quality report.
    
    Args:
        file_path: Path to the CSV file
        output_path: Optional path to save JSON report
        
    Returns:
        Dictionary containing the complete quality report
    """
    # Load data
    df = load_data(file_path)
    
    # Perform all checks
    missing_info = check_missing_values(df)
    duplicate_info = detect_duplicates(df)
    data_types = check_data_types(df)
    statistics = calculate_statistics(df)
    
    # Detect outliers for numeric columns
    outliers_info = {}
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    for column in numeric_columns:
        outliers = detect_outliers(df, column)
        if outliers:
            outliers_info[column] = outliers
    
    # Calculate quality score
    quality_score = calculate_quality_score(df, missing_info, duplicate_info['count'])
    
    # Build report
    report = {
        'file_name': file_path,
        'total_rows': int(len(df)),
        'total_columns': int(len(df.columns)),
        'columns': list(df.columns),
        'data_types': data_types,
        'missing_values': missing_info,
        'duplicates': duplicate_info,
        'outliers': outliers_info,
        'statistics': statistics,
        'quality_score': quality_score
    }
    
    # Save to file if output path provided
    if output_path:
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
    
    return report


# Command-line interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python data_analyzer.py <csv_file_path> [output_json_path]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "reports/quality_report.json"
    
    print(f"Analyzing data from: {input_file}")
    report = generate_quality_report(input_file, output_file)
    
    print(f"\n{'='*50}")
    print("DATA QUALITY REPORT")
    print(f"{'='*50}")
    print(f"Total Rows: {report['total_rows']}")
    print(f"Total Columns: {report['total_columns']}")
    print(f"Missing Values: {len(report['missing_values'])} columns affected")
    print(f"Duplicates: {report['duplicates']['count']} rows")
    print(f"Outliers: {len(report['outliers'])} columns with outliers")
    print(f"Quality Score: {report['quality_score']}/100")
    print(f"\nFull report saved to: {output_file}")