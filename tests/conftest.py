"""Pytest configuration and fixtures for Voynich Decryption tests."""

import json
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest

from voynich_decryption.models import AnalysisResult, Morpheme, MorphemeType, WordAnalysis


@pytest.fixture
def sample_morpheme() -> Morpheme:
    """Create a sample morpheme for testing."""
    return Morpheme(
        glyph="qo",
        morpheme_id="morpheme_001",
        morpheme_type=MorphemeType.ROOT,
        frequency=10,
        confidence_score=0.85,
        botanical_reference="plant_ref_01",
        pharmaceutical_use="medical_use_01",
    )


@pytest.fixture
def sample_morphemes() -> list[Morpheme]:
    """Create a list of sample morphemes for testing."""
    return [
        Morpheme(
            glyph="qo",
            morpheme_id="morpheme_001",
            morpheme_type=MorphemeType.ROOT,
            frequency=10,
            confidence_score=0.85,
        ),
        Morpheme(
            glyph="dy",
            morpheme_id="morpheme_002",
            morpheme_type=MorphemeType.PREFIX,
            frequency=5,
            confidence_score=0.70,
        ),
        Morpheme(
            glyph="ain",
            morpheme_id="morpheme_003",
            morpheme_type=MorphemeType.SUFFIX,
            frequency=8,
            confidence_score=0.90,
        ),
    ]


@pytest.fixture
def sample_word_analysis(sample_morphemes: list[Morpheme]) -> WordAnalysis:
    """Create a sample word analysis for testing."""
    return WordAnalysis(
        word_glyph="qodyain",
        word_id="word_001",
        morphemes=sample_morphemes,
        total_frequency=23,
        confidence=0.82,
        potential_meaning="botanical reference",
        verification_status="verified",
    )


@pytest.fixture
def sample_analysis_result(
    sample_morphemes: list[Morpheme],
    sample_word_analysis: WordAnalysis,
) -> AnalysisResult:
    """Create a sample analysis result for testing."""
    morpheme_inventory = {m.morpheme_id: m for m in sample_morphemes}

    return AnalysisResult(
        total_words_analyzed=10,
        total_unique_words=8,
        morphemes_identified=3,
        chi_square_statistic=15.234,
        p_value=0.023,
        morpheme_inventory=morpheme_inventory,
        word_analyses=[sample_word_analysis],
    )


@pytest.fixture
def temp_vocabulary_file() -> Generator[Path, None, None]:
    """Create a temporary vocabulary JSON file for testing."""
    vocabulary = {
        "word_001": "qodyain",
        "word_002": "qokeedy",
        "word_003": "dain",
        "word_004": "qokedy",
        "word_005": "qokain",
    }

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".json",
        delete=False,
        encoding="utf-8",
    ) as f:
        json.dump(vocabulary, f)
        temp_path = Path(f.name)

    yield temp_path

    # Cleanup
    if temp_path.exists():
        temp_path.unlink()


@pytest.fixture
def temp_morpheme_inventory_file(
    sample_morphemes: list[Morpheme],
) -> Generator[Path, None, None]:
    """Create a temporary morpheme inventory JSON file for testing."""
    inventory = {
        m.morpheme_id: {
            "glyph": m.glyph,
            "type": m.morpheme_type.value,
            "frequency": m.frequency,
            "confidence": m.confidence_score,
            "botanical_ref": m.botanical_reference,
            "pharmaceutical_use": m.pharmaceutical_use,
        }
        for m in sample_morphemes
    }

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".json",
        delete=False,
        encoding="utf-8",
    ) as f:
        json.dump(inventory, f)
        temp_path = Path(f.name)

    yield temp_path

    # Cleanup
    if temp_path.exists():
        temp_path.unlink()


@pytest.fixture
def temp_output_dir() -> Generator[Path, None, None]:
    """Create a temporary output directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def sample_vocabulary() -> dict[str, str]:
    """Create a sample vocabulary for testing."""
    return {
        "word_001": "qodyain",
        "word_002": "qokeedy",
        "word_003": "dain",
        "word_004": "qokedy",
        "word_005": "qokain",
        "word_006": "qol",
        "word_007": "dal",
        "word_008": "chedy",
        "word_009": "qokeey",
        "word_010": "shedy",
    }


@pytest.fixture
def mock_logger(monkeypatch):
    """Mock logger to suppress log output during tests."""
    import logging

    # Create a null handler
    null_handler = logging.NullHandler()

    # Mock the logger
    def mock_get_logger(name):
        logger = logging.getLogger(name)
        logger.handlers = [null_handler]
        logger.propagate = False
        return logger

    monkeypatch.setattr(logging, "getLogger", mock_get_logger)
