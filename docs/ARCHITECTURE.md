# Architecture Overview

## High-Level Design

```
┌─────────────┐
│   CLI       │ ← User interaction
└──────┬──────┘
       │
       ├──────────────┐
       │              │
┌──────▼──────┐  ┌───▼──────────┐
│  Analyzer   │  │ Config Parser│
└──────┬──────┘  └───┬──────────┘
       │             │
       └──────┬──────┘
              │
       ┌──────▼──────────┐
       │ Pipeline        │
       │ Generator       │
       └──────┬──────────┘
              │
       ┌──────▼──────────┐
       │ Template Engine │
       └──────┬──────────┘
              │
       ┌──────▼──────────┐
       │ Workflow File   │
       └─────────────────┘
```

## Components

### 1. Repository Analyzer

**Purpose**: Examines repository to detect languages, frameworks, and configuration

**Key Methods**:
- `analyze()` - Main entry point
- `_detect_languages()` - File extension analysis
- `_detect_frameworks()` - Framework indicator files
- `_has_dockerfile()` - Docker detection
- `_detect_package_manager()` - Package manager detection

**Output**: Analysis dictionary with detected features

### 2. Configuration Parser

**Purpose**: Loads and merges user configuration with defaults

**Key Methods**:
- `parse()` - Load config or use defaults
- `_find_config_file()` - Locate config in repo
- `_deep_merge()` - Merge user config with defaults

**Config Files**:
- `pipeline-config.yml` (primary)
- `.pipeline.yml` (alternate)

### 3. Pipeline Generator

**Purpose**: Creates CI/CD workflow files from analysis and config

**Key Methods**:
- `generate()` - Main generation logic
- `_select_template()` - Choose appropriate template
- `_generate_github_actions()` - GitHub-specific generation

**Templates**:
- `python-pipeline.yml.j2`
- `docker-pipeline.yml.j2`
- `node-pipeline.yml.j2`
- `generic-pipeline.yml.j2`

Uses Jinja2 for template rendering.

### 4. Security Scanner

**Purpose**: Orchestrates security scanning tools

**Key Methods**:
- `run_scans()` - Execute specified scanners
- `_run_trivy()` - Container scanning
- `_run_snyk()` - Dependency scanning
- `_run_sast()` - Static analysis

**Outputs**: JSON reports for each scanner

## Data Flow

1. User invokes CLI command
2. Analyzer scans repository structure
3. Config parser loads configuration
4. Generator selects template based on analysis
5. Template engine renders workflow file
6. Workflow file written to output directory

## Extension Points

Want to add new features? Here's where:

### New CI/CD Platform
- Add method to `PipelineGenerator`
- Create new template directory
- Update CLI platform option

### New Language Support
- Add extensions to `LANGUAGE_EXTENSIONS`
- Create language-specific template
- Update template selection logic

### New Security Scanner
- Add method to `SecurityScanner`
- Integrate scanner binary/API
- Update report aggregation

### New Framework Detection
- Add to `FRAMEWORK_INDICATORS`
- Create framework-specific template sections
- Update template variables

## Design Decisions

### Why Jinja2?
Template-based generation is flexible and maintainable. Easy to customize workflows without changing Python code.

### Why JSON for Reports?
Machine-readable format for integration with other tools. Easy to aggregate and analyze programmatically.

### Why Separate Analyzer?
Decouples detection logic from generation. Makes it easy to add new detection patterns without affecting generation.

## Performance Considerations

- Repository scanning can be slow for large repos (1000+ files)
- Currently walks entire directory tree
- TODO: Add caching for repeated analyses
- TODO: Parallel file scanning

## Testing Strategy

- Unit tests for each component
- Integration tests for full flow (TODO)
- Mock external tools (trivy, snyk) in tests
- Temporary directories for file I/O tests
