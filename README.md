# CI/CD Pipeline Generator 🚀

A tool that analyzes your repository and automatically generates CI/CD pipelines. Started as a side project to learn about different build systems and CI/CD patterns.

## What it does

- Analyzes repository structure and detects technologies
- Generates appropriate CI/CD pipelines (GitHub Actions, GitLab CI, etc.)
- Includes security scanning integration
- Supports multiple languages and frameworks

## Quick Start ⚡

```bash
# Install
pip install -e .

# Analyze a repo
pipeline-gen analyze /path/to/your/repo

# Generate pipeline
pipeline-gen generate /path/to/your/repo
```

## Features

- Automatic technology detection
- Multi-template support (Python, Node.js, Docker, etc.)
- Security scanning integration 🔒
- Extensible architecture
- CLI and programmatic API

## Architecture

The tool has three main components:
1. **Analyzer** - detects what tech stack is used
2. **Generator** - creates appropriate pipeline files
3. **Scanner** - optional security checks

## TODO

- Add GitLab CI support
- Better error messages
- Web dashboard (maybe)
- More framework detection

## Notes

This started as a weekend project but grew more complex than expected. The analyzer part was trickier to get right - detecting frameworks reliably is harder than it seems.

Based on patterns from various open-source projects I've worked with.