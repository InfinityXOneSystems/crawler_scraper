# Contributing to Crawler Scrapper

Thank you for your interest in contributing to the Crawler Scrapper project! This document provides guidelines and instructions for contributing.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip
- git

### Setting Up Development Environment

1. Fork the repository on GitHub

2. Clone your fork:
```bash
git clone https://github.com/YOUR_USERNAME/crawler_scrapper.git
cd crawler_scrapper
```

3. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
pip install -e ".[dev]"
```

## Development Workflow

### Creating a Branch

Create a new branch for your feature or fix:
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-fix-name
```

### Making Changes

1. Write your code following the project's coding standards
2. Add or update tests as necessary
3. Update documentation if needed
4. Run tests to ensure everything works

### Running Tests

Run all tests:
```bash
python -m pytest
```

Run specific test file:
```bash
python tests/test_scraper.py
```

Run with coverage:
```bash
pytest --cov=crawler_scrapper tests/
```

### Code Style

This project follows PEP 8 style guidelines. Please ensure your code adheres to these standards.

You can check your code style with:
```bash
flake8 src/
```

### Committing Changes

1. Stage your changes:
```bash
git add .
```

2. Commit with a descriptive message:
```bash
git commit -m "Add feature: description of your changes"
```

Follow these commit message guidelines:
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Start with a capital letter
- Keep first line under 50 characters
- Add detailed description after a blank line if needed

### Pushing Changes

Push your changes to your fork:
```bash
git push origin feature/your-feature-name
```

### Creating a Pull Request

1. Go to the original repository on GitHub
2. Click "New Pull Request"
3. Select your fork and branch
4. Fill in the PR template with:
   - Description of changes
   - Related issues
   - Testing done
   - Screenshots (if applicable)
5. Submit the pull request

## Contribution Guidelines

### Code Quality

- Write clean, readable, and maintainable code
- Follow the existing code structure and patterns
- Add comments for complex logic
- Use meaningful variable and function names

### Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Maintain or improve code coverage
- Test edge cases and error conditions

### Documentation

- Update README.md if adding new features
- Update API.md for API changes
- Add docstrings to all functions and classes
- Include examples in docstrings when helpful

### Module Development

When creating new modules:

1. Inherit from `BaseModule`
2. Implement all required methods
3. Add comprehensive docstrings
4. Include configuration validation
5. Write unit tests
6. Add usage examples

Example:
```python
from crawler_scrapper.core import BaseModule

class MyModule(BaseModule):
    """
    Description of what this module does.
    
    Args:
        config: Configuration dictionary with keys:
            - key1: description
            - key2: description
    """
    
    def initialize(self) -> bool:
        """Initialize the module."""
        # Your initialization code
        return True
    
    def execute(self, data):
        """
        Execute module logic.
        
        Args:
            data: Input data description
            
        Returns:
            Output data description
        """
        # Your execution code
        return data
    
    def cleanup(self):
        """Cleanup resources."""
        pass
```

### Integration Development

When creating new integrations:

1. Follow the same pattern as existing integrations
2. Implement mock/test mode
3. Handle errors gracefully
4. Document API endpoints and authentication
5. Add configuration examples

## Types of Contributions

### Bug Reports

When reporting bugs, include:
- Python version
- Operating system
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages and stack traces

### Feature Requests

When requesting features, include:
- Use case description
- Expected behavior
- Why this would be useful
- Any relevant examples

### Code Contributions

We welcome contributions for:
- Bug fixes
- New features
- Performance improvements
- Documentation improvements
- Test coverage improvements
- New modules and integrations

### Documentation Contributions

Documentation improvements are always welcome:
- Fix typos or unclear explanations
- Add examples
- Improve API documentation
- Add tutorials or guides

## Review Process

1. A maintainer will review your PR
2. They may request changes or ask questions
3. Address feedback by pushing new commits
4. Once approved, a maintainer will merge your PR

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discriminatory language
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information
- Unprofessional conduct

## Getting Help

If you need help:
- Check existing documentation
- Search existing issues
- Ask questions in issues with the "question" label
- Reach out to maintainers

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Credited in release notes
- Acknowledged in the README

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Questions?

If you have questions about contributing, please open an issue with the "question" label.

Thank you for contributing to Crawler Scrapper!
