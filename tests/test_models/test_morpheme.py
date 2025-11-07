"""Tests for Morpheme model."""

import pytest

from voynich_decryption.models import Morpheme, MorphemeType


class TestMorpheme:
    """Test suite for Morpheme class."""

    def test_create_morpheme(self):
        """Test creating a valid morpheme."""
        morpheme = Morpheme(
            glyph="qo",
            morpheme_id="test_001",
            morpheme_type=MorphemeType.ROOT,
            frequency=10,
            confidence_score=0.85,
        )

        assert morpheme.glyph == "qo"
        assert morpheme.morpheme_id == "test_001"
        assert morpheme.morpheme_type == MorphemeType.ROOT
        assert morpheme.frequency == 10
        assert morpheme.confidence_score == 0.85

    def test_morpheme_validation_confidence_above_one(self):
        """Test that confidence score above 1.0 raises ValueError."""
        with pytest.raises(ValueError, match="Confidence score must be between 0 and 1"):
            Morpheme(
                glyph="qo",
                morpheme_id="test_001",
                morpheme_type=MorphemeType.ROOT,
                confidence_score=1.5,
            )

    def test_morpheme_validation_confidence_below_zero(self):
        """Test that confidence score below 0.0 raises ValueError."""
        with pytest.raises(ValueError, match="Confidence score must be between 0 and 1"):
            Morpheme(
                glyph="qo",
                morpheme_id="test_001",
                morpheme_type=MorphemeType.ROOT,
                confidence_score=-0.1,
            )

    def test_morpheme_validation_negative_frequency(self):
        """Test that negative frequency raises ValueError."""
        with pytest.raises(ValueError, match="Frequency must be non-negative"):
            Morpheme(
                glyph="qo",
                morpheme_id="test_001",
                morpheme_type=MorphemeType.ROOT,
                frequency=-5,
            )

    def test_morpheme_validation_empty_glyph(self):
        """Test that empty glyph raises ValueError."""
        with pytest.raises(ValueError, match="Glyph cannot be empty"):
            Morpheme(
                glyph="",
                morpheme_id="test_001",
                morpheme_type=MorphemeType.ROOT,
            )

    def test_morpheme_validation_empty_id(self):
        """Test that empty morpheme_id raises ValueError."""
        with pytest.raises(ValueError, match="Morpheme ID cannot be empty"):
            Morpheme(
                glyph="qo",
                morpheme_id="",
                morpheme_type=MorphemeType.ROOT,
            )

    def test_morpheme_to_dict(self, sample_morpheme):
        """Test converting morpheme to dictionary."""
        data = sample_morpheme.to_dict()

        assert isinstance(data, dict)
        assert data["glyph"] == "qo"
        assert data["morpheme_id"] == "morpheme_001"
        assert data["type"] == "root"
        assert data["frequency"] == 10
        assert data["confidence"] == 0.85

    def test_morpheme_from_dict(self):
        """Test creating morpheme from dictionary."""
        data = {
            "glyph": "dy",
            "morpheme_id": "test_002",
            "type": "prefix",
            "frequency": 5,
            "confidence": 0.70,
        }

        morpheme = Morpheme.from_dict(data)

        assert morpheme.glyph == "dy"
        assert morpheme.morpheme_id == "test_002"
        assert morpheme.morpheme_type == MorphemeType.PREFIX
        assert morpheme.frequency == 5
        assert morpheme.confidence_score == 0.70

    def test_morpheme_str_representation(self, sample_morpheme):
        """Test string representation of morpheme."""
        s = str(sample_morpheme)
        assert "morpheme_001" in s
        assert "qo" in s
        assert "root" in s

    def test_morpheme_repr_representation(self, sample_morpheme):
        """Test repr representation of morpheme."""
        r = repr(sample_morpheme)
        assert "Morpheme" in r
        assert "qo" in r
        assert "morpheme_001" in r

    def test_morpheme_with_optional_fields(self):
        """Test creating morpheme with optional fields."""
        morpheme = Morpheme(
            glyph="qo",
            morpheme_id="test_001",
            morpheme_type=MorphemeType.ROOT,
            botanical_reference="Plant A",
            pharmaceutical_use="Remedy for X",
            historical_notes="Found in folio 1",
        )

        assert morpheme.botanical_reference == "Plant A"
        assert morpheme.pharmaceutical_use == "Remedy for X"
        assert morpheme.historical_notes == "Found in folio 1"


class TestMorphemeType:
    """Test suite for MorphemeType enum."""

    def test_morpheme_types(self):
        """Test all morpheme types."""
        assert MorphemeType.ROOT.value == "root"
        assert MorphemeType.PREFIX.value == "prefix"
        assert MorphemeType.SUFFIX.value == "suffix"
        assert MorphemeType.INFIX.value == "infix"
        assert MorphemeType.COMPOUND.value == "compound"
        assert MorphemeType.UNKNOWN.value == "unknown"

    def test_morpheme_type_from_string(self):
        """Test creating morpheme type from string value."""
        assert MorphemeType("root") == MorphemeType.ROOT
        assert MorphemeType("prefix") == MorphemeType.PREFIX
        assert MorphemeType("suffix") == MorphemeType.SUFFIX
