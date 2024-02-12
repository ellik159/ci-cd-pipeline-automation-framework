"""Tests for repository analyzer"""

import pytest
from pathlib import Path
import tempfile
import os

from src.analyzers.repo_analyzer import RepositoryAnalyzer


def test_analyzer_detects_python():
    """Test that analyzer correctly identifies Python projects"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a Python file
        py_file = Path(tmpdir) / 'main.py'
        py_file.write_text('print("hello")')
        
        analyzer = RepositoryAnalyzer(tmpdir)
        result = analyzer.analyze()
        
        assert 'python' in result['languages']


def test_analyzer_detects_dockerfile():
    """Test Docker detection"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create Dockerfile
        dockerfile = Path(tmpdir) / 'Dockerfile'
        dockerfile.write_text('FROM python:3.9')
        
        analyzer = RepositoryAnalyzer(tmpdir)
        result = analyzer.analyze()
        
        assert result['has_docker'] is True


def test_analyzer_detects_tests():
    """Test that analyzer finds test directories"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create tests directory
        tests_dir = Path(tmpdir) / 'tests'
        tests_dir.mkdir()
        (tests_dir / 'test_sample.py').write_text('def test_foo(): pass')
        
        analyzer = RepositoryAnalyzer(tmpdir)
        result = analyzer.analyze()
        
        assert result['has_tests'] is True


def test_analyzer_detects_pip():
    """Test package manager detection for pip"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create requirements.txt
        req_file = Path(tmpdir) / 'requirements.txt'
        req_file.write_text('flask==2.0.0\nrequests>=2.28.0')
        
        analyzer = RepositoryAnalyzer(tmpdir)
        result = analyzer.analyze()
        
        assert result['package_manager'] == 'pip'
        assert 'flask' in result['dependencies']
        assert 'requests' in result['dependencies']


def test_analyzer_handles_empty_repo():
    """Test analyzer with empty repository"""
    with tempfile.TemporaryDirectory() as tmpdir:
        analyzer = RepositoryAnalyzer(tmpdir)
        result = analyzer.analyze()
        
        assert result['languages'] == []
        assert result['has_docker'] is False
        assert result['has_tests'] is False
