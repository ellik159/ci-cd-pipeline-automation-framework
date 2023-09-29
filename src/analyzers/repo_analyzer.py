# Repository analyzer - figures out what tech a repo uses
# TODO: add more framework detection

import os
import json
from pathlib import Path
from typing import Dict, List, Set

class RepositoryAnalyzer:
    # file extensions for different languages
    LANGUAGE_EXTENSIONS = {
        'python': ['.py'],
        'javascript': ['.js', '.jsx'],
        'typescript': ['.ts', '.tsx'],
        'java': ['.java'],
        'go': ['.go'],
        'ruby': ['.rb'],
        'php': ['.php'],
    }
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
    
    def analyze(self) -> Dict:
        return {
            'languages': self._detect_languages(),
            'frameworks': [],
            'has_docker': self._has_dockerfile(),
            'has_tests': False,
        }
    
    def _detect_languages(self) -> List[str]:
        languages = set()
        for root, dirs, files in os.walk(self.repo_path):
            for file in files:
                ext = Path(file).suffix
                for lang, extensions in self.LANGUAGE_EXTENSIONS.items():
                    if ext in extensions:
                        languages.add(lang)
        return sorted(list(languages))
    
    def _has_dockerfile(self) -> bool:
        dockerfile = self.repo_path / 'Dockerfile'
        return dockerfile.exists()
