"""Tests for configuration parser"""

import pytest
from pathlib import Path
import tempfile

from src.config.config_parser import ConfigParser


def test_parser_uses_defaults_when_no_config():
    """Test that parser returns defaults when no config file exists"""
    with tempfile.TemporaryDirectory() as tmpdir:
        parser = ConfigParser(tmpdir)
        config = parser.parse()
        
        assert 'pipeline' in config
        assert 'security' in config
        assert config['pipeline']['name'] == 'CI/CD Pipeline'


def test_parser_loads_yaml_config():
    """Test that parser correctly loads YAML config"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create config file
        config_file = Path(tmpdir) / 'pipeline-config.yml'
        config_file.write_text("""
pipeline:
  name: Custom Pipeline
  triggers:
    - push

security:
  trivy_enabled: false
  snyk_enabled: true
""")
        
        parser = ConfigParser(tmpdir)
        config = parser.parse()
        
        assert config['pipeline']['name'] == 'Custom Pipeline'
        assert config['security']['snyk_enabled'] is True


def test_parser_merges_with_defaults():
    """Test that parser merges config with defaults"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = Path(tmpdir) / 'pipeline-config.yml'
        config_file.write_text("""
pipeline:
  name: My Pipeline
""")
        
        parser = ConfigParser(tmpdir)
        config = parser.parse()
        
        # Should have custom name
        assert config['pipeline']['name'] == 'My Pipeline'
        # But still have default triggers
        assert 'triggers' in config['pipeline']
