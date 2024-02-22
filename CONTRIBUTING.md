# Contribution Guidelines

Thanks for considering contributing! This is a personal project but contributions are welcome.

## How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest tests/`)
5. Commit your changes (`git commit -m 'Add some feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Code Style

- Follow PEP 8 for Python code (mostly)
- Use meaningful variable names
- Add docstrings for public functions
- Write tests for new features

## Running Tests

```bash
# Install dev dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src
```

## Reporting Bugs

Open an issue with:
- Description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version)

## Feature Requests

Open an issue describing:
- The feature you want
- Why it would be useful
- How it should work (if you have ideas)

## Questions?

Feel free to open an issue for questions about the codebase or usage.
