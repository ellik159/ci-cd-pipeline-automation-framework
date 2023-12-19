"""
Security scanner - integrates multiple security scanning tools
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List
import re


class SecurityScanner:
    """Orchestrates security scans using various tools"""
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        if not self.repo_path.exists():
            raise ValueError(f"Repository path does not exist: {repo_path}")
    
    def run_scans(self, scanners: List[str], output_dir: str) -> Dict:
        """Run specified security scanners"""
        results = {}
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        for scanner in scanners:
            if scanner == 'trivy':
                results['trivy'] = self._run_trivy(output_path)
            elif scanner == 'snyk':
                results['snyk'] = self._run_snyk(output_path)
            elif scanner == 'sast':
                results['sast'] = self._run_sast(output_path)
            else:
                results[scanner] = {'status': 'unknown', 'message': f'Unknown scanner: {scanner}'}
        
        return results
    
    def _run_trivy(self, output_path: Path) -> Dict:
        """Run Trivy container scanner"""
        # Check if Dockerfile exists
        dockerfile = self.repo_path / 'Dockerfile'
        
        if not dockerfile.exists():
            return {
                'status': 'skipped',
                'message': 'No Dockerfile found',
                'issues_found': 0
            }
        
        # Check if trivy is installed
        try:
            subprocess.run(['trivy', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            return {
                'status': 'error',
                'message': 'Trivy not installed',
                'issues_found': 0
            }
        
        # Run trivy scan
        try:
            output_file = output_path / 'trivy-report.json'
            result = subprocess.run(
                ['trivy', 'config', str(self.repo_path), '--format', 'json', '--output', str(output_file)],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            # Parse results
            issues = 0
            if output_file.exists():
                with open(output_file, 'r') as f:
                    data = json.load(f)
                    # Count vulnerabilities (this is simplified)
                    if 'Results' in data:
                        for result in data['Results']:
                            issues += len(result.get('Vulnerabilities', []))
            
            return {
                'status': 'success',
                'issues_found': issues,
                'report_file': str(output_file)
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'issues_found': 0
            }
    
    def _run_snyk(self, output_path: Path) -> Dict:
        """Run Snyk dependency scanner"""
        # Check for SNYK_TOKEN
        snyk_token = os.getenv('SNYK_TOKEN')
        
        if not snyk_token:
            return {
                'status': 'skipped',
                'message': 'SNYK_TOKEN environment variable not set',
                'issues_found': 0
            }
        
        # Check if snyk is installed
        try:
            subprocess.run(['snyk', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            return {
                'status': 'error',
                'message': 'Snyk CLI not installed',
                'issues_found': 0
            }
        
        # Run snyk test
        try:
            output_file = output_path / 'snyk-report.json'
            result = subprocess.run(
                ['snyk', 'test', '--json'],
                cwd=str(self.repo_path),
                capture_output=True,
                text=True,
                timeout=180
            )
            
            # Save output
            with open(output_file, 'w') as f:
                f.write(result.stdout)
            
            # Parse results
            try:
                data = json.loads(result.stdout)
                issues = len(data.get('vulnerabilities', []))
            except json.JSONDecodeError:
                issues = 0
            
            return {
                'status': 'success',
                'issues_found': issues,
                'report_file': str(output_file)
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'issues_found': 0
            }
    
    def _run_sast(self, output_path: Path) -> Dict:
        """Run basic SAST (Static Application Security Testing)"""
        # This is a simplified SAST implementation
        # Just scans for common security issues in code
        
        issues = []
        
        # Define security patterns to look for
        patterns = {
            'hardcoded_secrets': [
                (r'password\s*=\s*["\'][^"\']+["\']', 'Potential hardcoded password'),
                (r'api_key\s*=\s*["\'][^"\']+["\']', 'Potential hardcoded API key'),
                (r'secret\s*=\s*["\'][^"\']+["\']', 'Potential hardcoded secret'),
                (r'token\s*=\s*["\'][^"\']+["\']', 'Potential hardcoded token'),
            ],
            'sql_injection': [
                (r'execute\s*\(\s*["\'].*%s.*["\']', 'Potential SQL injection'),
                (r'\.format\s*\(.*SELECT.*\)', 'Potential SQL injection via format'),
            ],
            'command_injection': [
                (r'os\.system\s*\(', 'Use of os.system (potential command injection)'),
                (r'subprocess\.call\s*\(.*shell\s*=\s*True', 'subprocess with shell=True'),
            ],
        }
        
        # Scan Python files
        for root, dirs, files in os.walk(self.repo_path):
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'venv', '__pycache__']]
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            
                            for category, pattern_list in patterns.items():
                                for pattern, description in pattern_list:
                                    matches = re.finditer(pattern, content, re.IGNORECASE)
                                    for match in matches:
                                        # Get line number
                                        line_num = content[:match.start()].count('\n') + 1
                                        issues.append({
                                            'file': str(Path(file_path).relative_to(self.repo_path)),
                                            'line': line_num,
                                            'category': category,
                                            'description': description,
                                            'code': match.group(0)
                                        })
                    except (OSError, UnicodeDecodeError):
                        pass  # skip files we can't read
        
        # Save report
        output_file = output_path / 'sast-report.json'
        with open(output_file, 'w') as f:
            json.dump({'issues': issues}, f, indent=2)
        
        return {
            'status': 'success',
            'issues_found': len(issues),
            'report_file': str(output_file)
        }
