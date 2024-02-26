# Example Usage

## Basic Python Project

For a basic Python project with tests:

```bash
cd /path/to/your/python/project
python -m src.cli generate --repo-path . --output .github/workflows
```

This will:
1. Analyze your repository
2. Detect Python as the language
3. Generate a GitHub Actions workflow
4. Include security scanning (SAST)

## Docker Application

For a Dockerized application:

```bash
python -m src.cli generate --repo-path /path/to/docker/app --output .github/workflows
```

Will generate a workflow that:
- Builds Docker image
- Runs tests in container
- Scans with Trivy for vulnerabilities
- Pushes to Docker Hub on main branch

## Custom Configuration

Create a `pipeline-config.yml` in your repository:

```yaml
pipeline:
  name: "My Custom Pipeline"
  triggers:
    - push
    - pull_request

security:
  trivy_enabled: true
  snyk_enabled: true
  sast_enabled: true

runtime:
  python_version: "3.11"

notifications:
  slack_webhook: ${SLACK_WEBHOOK}
```

Then generate:

```bash
python -m src.cli generate --repo-path . --config pipeline-config.yml
```

## Security Scanning Only

To just run security scans without generating a pipeline:

```bash
python -m src.cli scan --repo-path . --scanners trivy,snyk,sast
```

Results will be saved in `security_reports/` directory.

## Repository Analysis

To see what the framework detects in your repository:

```bash
python -m src.cli analyze --repo-path .
```

This shows:
- Detected languages
- Frameworks
- Docker presence
- Test detection
- Package manager
