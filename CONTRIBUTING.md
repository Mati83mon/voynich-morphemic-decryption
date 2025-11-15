# Contributing to Voynich Morphemic Decryption

First off, thank you for considering contributing to Voynich Morphemic Decryption! 🎉

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Testing Guidelines](#testing-guidelines)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When you create a bug report, include as many details as possible:

- Use a clear and descriptive title
- Describe the exact steps to reproduce the problem
- Provide specific examples
- Describe the behavior you observed and what you expected
- Include Python version, OS, and relevant logs

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- Use a clear and descriptive title
- Provide a detailed description of the suggested enhancement
- Explain why this enhancement would be useful
- List any alternative solutions you've considered

### Pull Requests

- Fill in the pull request template
- Follow the Python style guide (PEP 8, Black formatting)
- Include tests for new functionality
- Update documentation as needed
- Ensure CI/CD passes

## Development Setup

### Prerequisites

- Python 3.11 or higher
- Poetry (recommended) or pip
- Git
- Docker (optional, for containerized development)

### Setup Steps

```bash
# Clone the repository
git clone https://github.com/mati83moni/voynich-morphemic-decryption.git
cd voynich-morphemic-decryption

# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Run linters
ruff check src/ tests/
black --check src/ tests/
mypy src/
```

### Using Docker

```bash
# Build Docker image
docker build -t voynich-analysis -f Docker/Dockerfile .

# Run tests in Docker
docker run --rm voynich-analysis pytest

# Start development server
docker-compose up
```

## Pull Request Process

1. **Fork the repository** and create your branch from `develop`

```bash
git checkout -b feature/amazing-feature develop
```

2. **Make your changes** following our style guidelines

3. **Add tests** for any new functionality

4. **Update documentation** including:
   - Docstrings in code
   - README.md if needed
   - CHANGELOG.md

5. **Run the test suite** and ensure everything passes:

```bash
# Run tests
pytest --cov=src/voynich_decryption

# Run linters
ruff check src/ tests/
black src/ tests/
mypy src/

# Run security checks
bandit -r src/
```

6. **Commit your changes** with clear, descriptive messages:

```bash
git add .
git commit -m "feat: add amazing new feature

- Detailed description of changes
- Why this change was needed
- Any breaking changes

Closes #123"
```

7. **Push to your fork** and submit a pull request

```bash
git push origin feature/amazing-feature
```

8. **Wait for review** - maintainers will review your PR and may request changes

## Style Guidelines

### Python Code Style

We follow PEP 8 with some modifications:

- **Line length**: 100 characters (Black default)
- **Formatting**: Use Black for automatic formatting
- **Linting**: Use Ruff for fast linting
- **Type hints**: Required for all functions (MyPy strict mode)
- **Docstrings**: Google style, required for all public functions

Example:

```python
def analyze_morphemes(
    word: str,
    inventory: dict[str, Morpheme],
    confidence_threshold: float = 0.5,
) -> WordAnalysis:
    """
    Analyze a word and decompose it into morphemes.

    Args:
        word: The word to analyze
        inventory: Dictionary of known morphemes
        confidence_threshold: Minimum confidence score (default: 0.5)

    Returns:
        WordAnalysis object containing decomposition results

    Raises:
        ValueError: If word is empty or invalid

    Example:
        >>> analyzer = MorphemicAnalyzer()
        >>> result = analyzer.analyze_morphemes("qodyain", inventory)
        >>> print(result.morpheme_count)
        3
    """
    # Implementation here
    pass
```

### Commit Message Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Example:

```
feat(api): add batch analysis endpoint

Add new endpoint for analyzing multiple words in a single request.
This improves performance for large-scale analysis.

Closes #42
```

### Documentation Style

- Use Markdown for documentation files
- Include code examples where appropriate
- Keep language clear and concise
- Update table of contents when adding sections

## Testing Guidelines

### Writing Tests

- Place tests in `tests/` directory mirroring `src/` structure
- Use descriptive test names: `test_<functionality>_<expected_behavior>`
- Use pytest fixtures for common setup
- Aim for 95%+ code coverage

Example:

```python
import pytest
from voynich_decryption.core import MorphemicAnalyzer

class TestMorphemicAnalyzer:
    """Test suite for MorphemicAnalyzer class."""

    def test_decompose_word_returns_morphemes(self, sample_analyzer):
        """Test that decompose_word returns list of morphemes."""
        result = sample_analyzer.decompose_word("test", "word_001")

        assert isinstance(result, WordAnalysis)
        assert len(result.morphemes) > 0
        assert result.word_id == "word_001"

    def test_decompose_empty_word_raises_error(self, sample_analyzer):
        """Test that decomposing empty word raises ValueError."""
        with pytest.raises(ValueError, match="Word glyph cannot be empty"):
            sample_analyzer.decompose_word("", "word_001")
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_core/test_morphemic_analyzer.py

# Run with coverage
pytest --cov=src/voynich_decryption --cov-report=html

# Run with verbose output
pytest -v

# Run only failed tests
pytest --lf
```

## Questions?

Feel free to:
- Open an issue for questions
- Join discussions in GitHub Discussions
- Contact maintainers: mateuszpiesiak1990@gmail.com

Thank you for contributing! 🙏
