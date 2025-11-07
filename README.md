# Voynich Morphemic Decryption

[![CI/CD Pipeline](https://github.com/mati83moni/voynich-morphemic-decryption/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/mati83moni/voynich-morphemic-decryption/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Advanced morphemic analysis and decryption system for the Voynich Manuscript using statistical methods, machine learning, and computational linguistics.

## 🎯 Overview

This project implements a comprehensive analysis pipeline for the Voynich Manuscript, decomposing its text into morphemic units and performing statistical validation to identify patterns and potential meanings.

### Key Features

- **Morphemic Decomposition**: Advanced algorithms for breaking down Voynich words into constituent morphemes
- **Statistical Validation**: Chi-square tests, distribution analysis, and significance testing
- **REST API**: FastAPI-based web service for programmatic access
- **Batch Processing**: Analyze entire vocabularies efficiently
- **Comprehensive Reporting**: JSON, CSV, and text reports with visualizations
- **Docker Support**: Containerized deployment for reproducibility
- **CI/CD Pipeline**: Automated testing and quality assurance
- **Zenodo Integration**: Automatic DOI minting for research outputs

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Architecture](#architecture)
- [Testing](#testing)
- [Docker Deployment](#docker-deployment)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Installation

### Prerequisites

- Python 3.11 or higher
- pip or Poetry package manager
- Git

### Using pip

```bash
# Clone the repository
git clone https://github.com/mati83moni/voynich-morphemic-decryption.git
cd voynich-morphemic-decryption

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Using Poetry (Recommended)

```bash
# Clone the repository
git clone https://github.com/mati83moni/voynich-morphemic-decryption.git
cd voynich-morphemic-decryption

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

## ⚡ Quick Start

### Command Line Analysis

```bash
# Run analysis on vocabulary
python scripts/run_analysis.py

# Or use the CLI
voynich analyze --vocabulary data/voynich_full_vocabulary.json --output output/
```

### Python API

```python
from voynich_decryption import VoynichAnalysisPipeline

# Initialize pipeline
pipeline = VoynichAnalysisPipeline(config={
    "significance_threshold": 0.05,
    "output_dir": "./output",
    "verbose": True,
})

# Run analysis
result = pipeline.execute(
    vocabulary_file="data/voynich_full_vocabulary.json",
    generate_reports=True,
)

# Print summary
print(result.get_summary_report())
```

### REST API

```bash
# Start the API server
uvicorn voynich_decryption.api.app:app --reload

# Or use Docker
docker-compose up
```

Access the API documentation at http://localhost:8000/docs

## 📖 Usage

### Analyzing a Vocabulary

```python
from voynich_decryption import MorphemicAnalyzer, AnalysisResult

# Create analyzer
analyzer = MorphemicAnalyzer(verbose=True)

# Load morpheme inventory (optional)
analyzer.load_vocabulary("data/processed/morpheme_analysis_complete.json")

# Analyze vocabulary
vocabulary = {
    "word_001": "qodyain",
    "word_002": "qokeedy",
    "word_003": "dain",
}

result = analyzer.analyze_vocabulary(vocabulary)

# Access results
print(f"Words analyzed: {result.total_words_analyzed}")
print(f"Morphemes identified: {result.morphemes_identified}")
print(f"Statistically significant: {result.is_statistically_significant}")
```

### Decomposing Individual Words

```python
from voynich_decryption import MorphemicAnalyzer

analyzer = MorphemicAnalyzer()

# Decompose a single word
analysis = analyzer.decompose_word("qodyain", "word_001")

# View morphemes
for morpheme in analysis.morphemes:
    print(f"{morpheme.glyph} ({morpheme.morpheme_type.value})")
```

### Statistical Validation

```python
from voynich_decryption import StatisticalValidator

validator = StatisticalValidator(significance_threshold=0.05)

# Validate analysis results
validation = validator.validate_morphemic_patterns(result)

# Generate report
report = validator.generate_validation_report(validation)
print(report)
```

## 🌐 API Documentation

### Endpoints

- `GET /api/v1/health` - Health check
- `POST /api/v1/analyze` - Analyze vocabulary (summary)
- `POST /api/v1/analyze/detailed` - Detailed analysis with full results
- `POST /api/v1/decompose` - Decompose single word
- `GET /api/v1/statistics` - Get analyzer statistics
- `POST /api/v1/cache/clear` - Clear analyzer cache

### Example API Request

```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "vocabulary": {
      "word_001": "qodyain",
      "word_002": "qokeedy"
    },
    "significance_threshold": 0.05
  }'
```

## 🏗️ Architecture

```
src/voynich_decryption/
├── core/                    # Core analysis engines
│   ├── morphemic_analyzer.py
│   └── statistical_validator.py
├── models/                  # Data models
│   ├── morpheme.py
│   ├── word_analysis.py
│   └── analysis_result.py
├── pipelines/              # Analysis pipelines
│   ├── analysis_pipeline.py
│   └── reporting_pipeline.py
├── api/                    # REST API
│   ├── app.py
│   ├── routes.py
│   └── schemas.py
└── utils/                  # Utilities
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/voynich_decryption --cov-report=html

# Run specific test file
pytest tests/test_core/test_morphemic_analyzer.py -v

# Run integration tests
pytest tests/integration/ -v
```

### Test Coverage

The project maintains >95% test coverage across all modules.

## 🐳 Docker Deployment

### Build and Run

```bash
# Build Docker image
docker build -t voynich-analysis -f Docker/Dockerfile .

# Run container
docker run -p 8000:8000 voynich-analysis

# Or use Docker Compose
docker-compose up -d
```

### Environment Variables

See `.env.example` for configuration options:

```bash
cp .env.example .env
# Edit .env with your configuration
```

## 📊 Zenodo Integration

Publish analysis results to Zenodo for DOI minting:

```bash
# Set Zenodo token
export ZENODO_TOKEN="your_zenodo_token"

# Publish (sandbox mode)
python scripts/deploy_zenodo.py

# Publish to production
export ZENODO_SANDBOX=false
python scripts/deploy_zenodo.py
```

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run linting
ruff check src/ tests/

# Format code
black src/ tests/

# Type checking
mypy src/
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Mateusz Piesiak**
- Email: mateuszpiesiak1990@gmail.com
- GitHub: [@mati83moni](https://github.com/mati83moni)

## 📚 Citation

If you use this software in your research, please cite:

```bibtex
@software{piesiak2025voynich,
  author = {Piesiak, Mateusz},
  title = {Voynich Morphemic Decryption},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/mati83moni/voynich-morphemic-decryption}
}
```

## 🙏 Acknowledgments

- The Voynich Manuscript research community
- Beinecke Rare Book & Manuscript Library, Yale University
- Open source contributors

## 📈 Project Status

This project is actively maintained and under continuous development.

## 🔗 Related Resources

- [Voynich Manuscript (Yale)](https://collections.library.yale.edu/catalog/2002046)
- [Methodology Guide](docs/03_METHODOLOGY.md)
- [API Reference](docs/02_API_REFERENCE.md)

---

**Note**: This is a research project. Results should be interpreted with appropriate scientific rigor and peer review.
