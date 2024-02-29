"""
Quick script to test the analyzer locally
Used during development
"""

from src.analyzers.repo_analyzer import RepositoryAnalyzer
import json

def main():
    # Test on this project itself
    analyzer = RepositoryAnalyzer('.')
    result = analyzer.analyze()
    
    print("Analysis Results:")
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
