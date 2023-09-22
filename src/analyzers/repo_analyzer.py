# Repository analyzer - figures out what tech a repo uses
# TODO: add more framework detection, this is getting complex

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
    
    # framework indicators
    FRAMEWORK_INDICATORS = {
        'django': ['requirements.txt', 'manage.py'],
        'flask': ['requirements.txt', 'app.py'],
        'react': ['package.json', 'src/'],
        'vue': ['package.json', 'vue.config.js'],
    }
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
    
    
   self.repo_path = Path(repo_path)
ig.js'],  ig.js'],  ig.js'],  ig.js'],  ig.js'],  ig.js'],  ig.       'frameworks': self._detect_frameworks(),
            'has_docker': self._has_dockerfile(),
            'has_tests': self._has_tests(),
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
    
    def _detect_frameworks(self) -> List[str]:
        frameworks = []
        for framework, indicators in self.FRAMEWORK_INDICATORS.items():
            for indicator in indicators:
                if (self.repo_path / indicator).exists():
                    frameworks.append(framework)
                    break
        return frameworks
    
    def _has_dockerfile(self) -> bool:
        dockerfile = self.repo_path / 'Dockerfile'
        return dockerfile.exists()
    
    def _has_tests(self) -> bool:
        # simple test detection
        test_dirs = ['tests', 'test', '__tests__']
        for test_dir in test_dirs:
            if (self.repo_path / test_dir).exists():
                return True
        return False
