"""
Configuration parser - reads and validates pipeline configuration
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Optional


class ConfigParser:
    """Parses pipeline configuration from YAML files"""
    
    DEFAULT_CONFIG = {
        'pipeline': {
            'name': 'CI/CD Pipeline',
            'triggers': ['push', 'pull_request'],
        },
        'security': {
            'trivy_enabled': True,
            'snyk_enabled': False,
            'sast_enabled': True,
        },
        'runtime': {
            'python_version': '3.9',
            'node_version': '16',
        },
        'notifications': {},
    }
    
    def __init__(self, repo_path: str, config_file: Optional[str] = None):
        self.repo_path = Path(repo_path)
        self.config_file = config_file
    
    def parse(self) -> Dict:
        """Parse configuration file or use defaults"""
        
        # Try to find config file
        config_path = self._find_config_file()
        
        if config_path and config_path.exists():
            return self._load_config(config_path)
        else:
            # Use defaults
            return self.DEFAULT_CONFIG.copy()
    
    def _find_config_file(self) -> Optional[Path]:
        """Find configuration file in repository"""
        
        # If config file explicitly provided, use it
        if self.config_file:
            return Path(self.config_file)
        
        # Look for common config file names
        config_names = [
            'pipeline-config.yml',
            'pipeline-config.yaml',
            '.pipeline.yml',
            'ci-config.yml',
        ]
        
        for name in config_names:
            config_path = self.repo_path / name
            if config_path.exists():
                return config_path
        
        return None
    
    def _load_config(self, config_path: Path) -> Dict:
        """Load and parse YAML configuration file"""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            # Merge with defaults (for missing keys)
            merged_config = self.DEFAULT_CONFIG.copy()
            if config:
                self._deep_merge(merged_config, config)
            
            return merged_config
        except Exception as e:
            # If config file is invalid, use defaults
            print(f"Warning: Could not parse config file: {e}")
            return self.DEFAULT_CONFIG.copy()
    
    def _deep_merge(self, base: Dict, override: Dict) -> None:
        """Deep merge override dict into base dict"""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
