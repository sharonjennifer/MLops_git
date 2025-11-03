import pytest
import pandas as pd
import os
import json
from src.data_analyzer import (
    load_data,
    check_missing_values,
    detect_duplicates,
    detect_outliers,
    calculate_statistics,
    check_data_types,
    calculate_quality_score,
    generate_quality_report
)


# Test data paths
CLEAN_DATA_PATH = "data/raw/sample_clean.csv"
ISSUES_DATA_PATH = "data/raw/sample_with_issues.csv"


class TestLoadData:
    """Tests for load_data function"""
    
    def test_load_clean_data(self):
        """Test loading clean CSV file"""
        df = load_data(CLEAN_DATA_PATH)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 10
        assert len(df.columns) == 6
    
    def test_load_data_with_issues(self):
        """Test loading CSV file with quality issues"""
        df = load_data(ISSUES_DATA_PATH)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 12
    
    def test_load_nonexistent_file(self):
        """Test loading a file that doesn't exist"""
        with pytest.raises(FileNotFoundError):
            load_data("nonexistent_file.csv")


class TestMissingValues:
    """Tests for check_missing_values function"""
    
    def test_no_missing_values(self):
        """Test dataset with no missing values"""
        df = load_data(CLEAN_DATA_PATH)
        missing = check_missing_values(df)
        assert missing == {}
    
    def test_with_missing_values(self):
        """Test dataset with missing values"""
        df = load_data(ISSUES_DATA_PATH)
        missing = check_missing_values(df)
        assert len(missing) > 0
        assert 'age' in missing
        assert 'salary' in missing
        assert missing['age']['count'] > 0
        assert 0 <= missing['age']['percentage'] <= 100


class TestDuplicates:
    """Tests for detect_duplicates function"""
    
    def test_no_duplicates(self):
        """Test dataset with no duplicates"""
        df = load_data(CLEAN_DATA_PATH)
        duplicates = detect_duplicates(df)
        assert duplicates['count'] == 0
        assert duplicates['indices'] == []
    
    def test_with_duplicates(self):
        """Test dataset with duplicates"""
        df = load_data(ISSUES_DATA_PATH)
        duplicates = detect_duplicates(df)
        assert duplicates['count'] > 0
        assert len(duplicates['indices']) > 0


class TestOutliers:
    """Tests for detect_outliers function"""
    
    def test_no_outliers_clean_data(self):
        """Test clean data with no outliers"""
        df = load_data(CLEAN_DATA_PATH)
        outliers = detect_outliers(df, 'age')
        assert isinstance(outliers, list)
        assert len(outliers) == 0
    
    def test_with_outliers(self):
        """Test data with outliers"""
        df = load_data(ISSUES_DATA_PATH)
        outliers = detect_outliers(df, 'age')
        assert isinstance(outliers, list)
        assert len(outliers) > 0
        # Check for extreme values
        assert any(val > 100 or val < 0 for val in outliers)
    
    def test_outliers_invalid_column(self):
        """Test with non-existent column"""
        df = load_data(CLEAN_DATA_PATH)
        with pytest.raises(ValueError):
            detect_outliers(df, 'nonexistent_column')
    
    def test_outliers_zscore_method(self):
        """Test outlier detection with z-score method"""
        df = load_data(ISSUES_DATA_PATH)
        outliers = detect_outliers(df, 'salary', method='zscore')
        assert isinstance(outliers, list)


class TestStatistics:
    """Tests for calculate_statistics function"""
    
    def test_statistics_clean_data(self):
        """Test statistics calculation on clean data"""
        df = load_data(CLEAN_DATA_PATH)
        stats = calculate_statistics(df)
        
        assert 'age' in stats
        assert 'salary' in stats
        assert 'mean' in stats['age']
        assert 'median' in stats['age']
        assert 'std' in stats['age']
        assert 'min' in stats['age']
        assert 'max' in stats['age']
        
        # Verify reasonable values
        assert stats['age']['mean'] > 0
        assert stats['age']['min'] <= stats['age']['max']
    
    def test_statistics_with_missing_values(self):
        """Test statistics with missing values (should exclude NaN)"""
        df = load_data(ISSUES_DATA_PATH)
        stats = calculate_statistics(df)
        
        # Should still calculate stats, just excluding NaN
        assert 'age' in stats
        assert stats['age']['mean'] > 0


class TestDataTypes:
    """Tests for check_data_types function"""
    
    def test_data_types(self):
        """Test data type detection"""
        df = load_data(CLEAN_DATA_PATH)
        dtypes = check_data_types(df)
        
        assert 'id' in dtypes
        assert 'name' in dtypes
        assert 'age' in dtypes
        assert len(dtypes) == 6


class TestQualityScore:
    """Tests for calculate_quality_score function"""
    
    def test_perfect_score(self):
        """Test quality score for clean data"""
        df = load_data(CLEAN_DATA_PATH)
        missing_info = check_missing_values(df)
        duplicate_count = detect_duplicates(df)['count']
        
        score = calculate_quality_score(df, missing_info, duplicate_count)
        assert score == 100.0
    
    def test_reduced_score_with_issues(self):
        """Test quality score with data issues"""
        df = load_data(ISSUES_DATA_PATH)
        missing_info = check_missing_values(df)
        duplicate_count = detect_duplicates(df)['count']
        
        score = calculate_quality_score(df, missing_info, duplicate_count)
        assert 0 <= score < 100.0


class TestGenerateQualityReport:
    """Tests for generate_quality_report function"""
    
    def test_report_generation_clean_data(self):
        """Test full report generation for clean data"""
        output_path = "reports/test_clean_report.json"
        report = generate_quality_report(CLEAN_DATA_PATH, output_path)
        
        # Check report structure
        assert 'file_name' in report
        assert 'total_rows' in report
        assert 'total_columns' in report
        assert 'missing_values' in report
        assert 'duplicates' in report
        assert 'outliers' in report
        assert 'statistics' in report
        assert 'quality_score' in report
        
        # Verify values for clean data
        assert report['total_rows'] == 10
        assert report['quality_score'] == 100.0
        assert report['duplicates']['count'] == 0
        
        # Check if file was created
        assert os.path.exists(output_path)
        
        # Clean up
        os.remove(output_path)
    
    def test_report_generation_with_issues(self):
        """Test full report generation for data with issues"""
        output_path = "reports/test_issues_report.json"
        report = generate_quality_report(ISSUES_DATA_PATH, output_path)
        
        # Verify issues are detected
        assert len(report['missing_values']) > 0
        assert report['duplicates']['count'] > 0
        assert len(report['outliers']) > 0
        assert report['quality_score'] < 100.0
        
        # Check if file was created and is valid JSON
        assert os.path.exists(output_path)
        with open(output_path, 'r') as f:
            loaded_report = json.load(f)
            assert loaded_report == report
        
        # Clean up
        os.remove(output_path)
    
    def test_report_without_output_file(self):
        """Test report generation without saving to file"""
        report = generate_quality_report(CLEAN_DATA_PATH)
        assert report is not None
        assert 'quality_score' in report


# Integration tests
class TestIntegration:
    """Integration tests for the complete workflow"""
    
    def test_complete_workflow_clean_data(self):
        """Test complete analysis workflow on clean data"""
        # Load
        df = load_data(CLEAN_DATA_PATH)
        
        # Analyze
        missing = check_missing_values(df)
        duplicates = detect_duplicates(df)
        stats = calculate_statistics(df)
        
        # Verify clean data results
        assert len(missing) == 0
        assert duplicates['count'] == 0
        assert len(stats) > 0
    
    def test_complete_workflow_problematic_data(self):
        """Test complete analysis workflow on problematic data"""
        # Load
        df = load_data(ISSUES_DATA_PATH)
        
        # Analyze
        missing = check_missing_values(df)
        duplicates = detect_duplicates(df)
        outliers_age = detect_outliers(df, 'age')
        
        # Verify issues are detected
        assert len(missing) > 0
        assert duplicates['count'] > 0
        assert len(outliers_age) > 0