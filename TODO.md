# Project TODOs

## High Priority
- [ ] Add support for GitLab CI templates
- [ ] Add support for Jenkins pipeline generation
- [ ] Better error messages when analysis fails
- [ ] Performance optimization for large repositories (1000+ files)

## Medium Priority
- [ ] Web dashboard improvements (currently very minimal)
- [ ] Pipeline optimization suggestions based on repo size
- [ ] Support for monorepo detection and handling
- [ ] Add more SAST rules (currently pretty basic)
- [ ] Custom SAST pattern configuration via config file
- [ ] Integration tests for full workflow

## Low Priority
- [ ] Support for CircleCI
- [ ] Support for Azure Pipelines
- [ ] Notification integrations (Slack, Email, Discord)
- [ ] Pipeline visualization
- [ ] Historical security scan tracking
- [ ] Comparison between scans

## Code Quality
- [ ] Increase test coverage (currently ~50%)
- [ ] Add integration tests
- [ ] Better documentation for template customization
- [ ] Type hints throughout codebase
- [ ] Proper logging instead of print statements

## Known Issues
- Large repos take a long time to analyze (no progress indicator)
- Template selection logic could be smarter
- SAST has false positives on commented code
- Snyk integration requires manual token setup (should document better)
- Dashboard is just a placeholder

## Nice to Have
- [ ] VS Code extension for pipeline generation
- [ ] GitHub Action that auto-generates pipelines
- [ ] Cache analysis results to speed up repeated runs
- [ ] Parallel file scanning for better performance
- [ ] Support for custom template directories
