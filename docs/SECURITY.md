# Security Integration Guide

## Overview

The framework integrates three types of security scanning:

1. **Trivy** - Container vulnerability scanning
2. **Snyk** - Dependency vulnerability scanning
3. **SAST** - Static application security testing

## Trivy Setup

Trivy is used for scanning Docker images and container configurations.

### Installation

```bash
# Linux
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy

# macOS
brew install aquasecurity/trivy/trivy
```

### Usage

Trivy runs automatically when:
- Your repository contains a Dockerfile
- `trivy_enabled: true` in config

No additional configuration needed.

## Snyk Setup

Snyk scans your application dependencies for known vulnerabilities.

### Installation

```bash
npm install -g snyk
```

### Authentication

```bash
# Get your token from https://app.snyk.io/account
export SNYK_TOKEN=your-token-here
```

### Usage in CI/CD

Add `SNYK_TOKEN` as a GitHub secret:

1. Go to repository Settings → Secrets
2. Add new secret: `SNYK_TOKEN`
3. Enable in config: `snyk_enabled: true`

## SAST (Static Analysis)

Built-in SAST scans for common security issues:

- Hardcoded secrets (API keys, passwords, tokens)
- SQL injection patterns
- Command injection vulnerabilities
- Use of unsafe functions

### Patterns Detected

Currently detects:
- `password = "..."`
- `api_key = "..."`
- `os.system(...)` 
- `subprocess.call(..., shell=True)`
- SQL injection via string formatting

### Limitations

This is a basic SAST implementation. For production use, consider:
- SonarQube
- Semgrep
- Bandit (Python-specific)
- Commercial SAST tools

### Customization

TODO: Add ability to define custom patterns in config file

## Security Reports

All scan results are saved in JSON format:

```
security_reports/
  ├── trivy-report.json
  ├── snyk-report.json
  └── sast-report.json
```

These can be integrated with:
- GitHub Security tab
- Slack notifications
- Custom dashboards

## Best Practices

1. Run security scans on every PR
2. Set severity thresholds (high/critical only)
3. Don't block builds on low-severity issues
4. Review false positives regularly
5. Keep security tools updated

## GitHub Actions Integration

Security scans run as separate jobs:

```yaml
- sast-scan (always runs)
- snyk-scan (if configured)
- trivy-scan (for Docker projects)
```

Results upload to GitHub Security tab automatically (SARIF format).
