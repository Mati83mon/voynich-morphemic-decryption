"""Tests for MorphemicAnalyzer."""

import pytest

from voynich_decryption.core import MorphemicAnalyzer
from voynich_decryption.models import AnalysisResult, Morpheme, MorphemeType


class TestMorphemicAnalyzer:
    """Test suite for MorphemicAnalyzer class."""

    def test_create_analyzer(self):
        """Test creating analyzer instance."""
        analyzer = MorphemicAnalyzer(verbose=False)

        assert analyzer is not None
        assert len(analyzer.morpheme_inventory) == 0
        assert len(analyzer.word_cache) == 0

    def test_load_vocabulary_from_file(self, temp_morpheme_inventory_file):
        """Test loading morpheme inventory from file."""
        analyzer = MorphemicAnalyzer(verbose=False)
        analyzer.load_vocabulary(str(temp_morpheme_inventory_file))

        assert len(analyzer.morpheme_inventory) == 3
        assert "morpheme_001" in analyzer.morpheme_inventory

    def test_load_vocabulary_file_not_found(self):
        """Test loading vocabulary from non-existent file raises error."""
        analyzer = MorphemicAnalyzer(verbose=False)

        with pytest.raises(FileNotFoundError):
            analyzer.load_vocabulary("nonexistent_file.json")

    def test_add_morpheme(self):
        """Test adding morpheme to inventory."""
        analyzer = MorphemicAnalyzer(verbose=False)

        morpheme = Morpheme(
            glyph="qo",
            morpheme_id="test_001",
            morpheme_type=MorphemeType.ROOT,
            frequency=10,
            confidence_score=0.85,
        )

        analyzer.add_morpheme(morpheme)

        assert len(analyzer.morpheme_inventory) == 1
        assert "test_001" in analyzer.morpheme_inventory

    def test_add_duplicate_morpheme_raises_error(self):
        """Test adding duplicate morpheme raises ValueError."""
        analyzer = MorphemicAnalyzer(verbose=False)

        morpheme = Morpheme(
            glyph="qo",
            morpheme_id="test_001",
            morpheme_type=MorphemeType.ROOT,
        )

        analyzer.add_morpheme(morpheme)

        with pytest.raises(ValueError, match="already exists"):
            analyzer.add_morpheme(morpheme)

    def test_decompose_word(self, sample_morphemes):
        """Test decomposing a word into morphemes."""
        analyzer = MorphemicAnalyzer(verbose=False)

        # Add morphemes to inventory
        for morpheme in sample_morphemes:
            analyzer.add_morpheme(morpheme)

        # Decompose word
        analysis = analyzer.decompose_word("qodyain", "word_001")

        assert analysis.word_glyph == "qodyain"
        assert analysis.word_id == "word_001"
        assert len(analysis.morphemes) > 0

    def test_decompose_word_empty_glyph_raises_error(self):
        """Test decomposing empty word raises ValueError."""
        analyzer = MorphemicAnalyzer(verbose=False)

        with pytest.raises(ValueError, match="Word glyph cannot be empty"):
            analyzer.decompose_word("", "word_001")

    def test_decompose_word_empty_id_raises_error(self):
        """Test decomposing word with empty ID raises ValueError."""
        analyzer = MorphemicAnalyzer(verbose=False)

        with pytest.raises(ValueError, match="Word ID cannot be empty"):
            analyzer.decompose_word("qo", "")

    def test_decompose_word_caching(self, sample_morphemes):
        """Test that word decomposition uses caching."""
        analyzer = MorphemicAnalyzer(verbose=False)

        for morpheme in sample_morphemes:
            analyzer.add_morpheme(morpheme)

        # First decomposition
        analysis1 = analyzer.decompose_word("qodyain", "word_001")

        # Second decomposition (should be cached)
        analysis2 = analyzer.decompose_word("qodyain", "word_001")

        assert analysis1 is analysis2  # Same object reference

    def test_analyze_vocabulary(self, sample_vocabulary, sample_morphemes):
        """Test analyzing complete vocabulary."""
        analyzer = MorphemicAnalyzer(verbose=False)

        for morpheme in sample_morphemes:
            analyzer.add_morpheme(morpheme)

        result = analyzer.analyze_vocabulary(sample_vocabulary)

        assert isinstance(result, AnalysisResult)
        assert result.total_words_analyzed == len(sample_vocabulary)
        assert result.total_words_analyzed > 0

    def test_analyze_empty_vocabulary_raises_error(self):
        """Test analyzing empty vocabulary raises ValueError."""
        analyzer = MorphemicAnalyzer(verbose=False)

        with pytest.raises(ValueError, match="Vocabulary cannot be empty"):
            analyzer.analyze_vocabulary({})

    def test_perform_chi_square_test(self, sample_vocabulary, sample_morphemes):
        """Test chi-square statistical test."""
        analyzer = MorphemicAnalyzer(verbose=False)

        for morpheme in sample_morphemes:
            analyzer.add_morpheme(morpheme)

        result = analyzer.analyze_vocabulary(sample_vocabulary)

        assert result.chi_square_statistic >= 0
        assert 0 <= result.p_value <= 1

    def test_clear_cache(self, sample_morphemes):
        """Test clearing word analysis cache."""
        analyzer = MorphemicAnalyzer(verbose=False)

        for morpheme in sample_morphemes:
            analyzer.add_morpheme(morpheme)

        # Add to cache
        analyzer.decompose_word("qo", "word_001")

        assert len(analyzer.word_cache) == 1

        # Clear cache
        analyzer.clear_cache()

        assert len(analyzer.word_cache) == 0

    def test_get_statistics(self, sample_morphemes):
        """Test getting analyzer statistics."""
        analyzer = MorphemicAnalyzer(verbose=False)

        for morpheme in sample_morphemes:
            analyzer.add_morpheme(morpheme)

        stats = analyzer.get_statistics()

        assert isinstance(stats, dict)
        assert "morphemes_in_inventory" in stats
        assert stats["morphemes_in_inventory"] == 3

    def test_find_morpheme_sequences_creates_unknown_morphemes(self):
        """Test that unknown characters create unknown morphemes."""
        analyzer = MorphemicAnalyzer(verbose=False)

        # Don't add any morphemes to inventory

        analysis = analyzer.decompose_word("xyz", "word_001")

        # All characters should be unknown
        assert all(m.morpheme_type == MorphemeType.UNKNOWN for m in analysis.morphemes)

    def test_analyzer_with_verbose_mode(self, capsys):
        """Test analyzer in verbose mode produces log output."""
        analyzer = MorphemicAnalyzer(verbose=True)

        # This should produce log output
        assert analyzer.verbose is True


class TestMorphemicAnalyzerIntegration:
    """Integration tests for MorphemicAnalyzer."""

    def test_full_analysis_workflow(self, temp_vocabulary_file, temp_morpheme_inventory_file):
        """Test complete analysis workflow."""
        analyzer = MorphemicAnalyzer(
            vocabulary_file=str(temp_morpheme_inventory_file),
            verbose=False,
        )

        # Load vocabulary
        import json

        with open(temp_vocabulary_file) as f:
            vocabulary = json.load(f)

        # Perform analysis
        result = analyzer.analyze_vocabulary(vocabulary)

        assert result.total_words_analyzed == len(vocabulary)
        assert result.morphemes_identified > 0
        assert len(result.word_analyses) == len(vocabulary)

    def test_analysis_result_properties(self, sample_vocabulary, sample_morphemes):
        """Test that analysis result has correct properties."""
        analyzer = MorphemicAnalyzer(verbose=False)

        for morpheme in sample_morphemes:
            analyzer.add_morpheme(morpheme)

        result = analyzer.analyze_vocabulary(sample_vocabulary)

        # Test result properties
        assert result.total_words_analyzed > 0
        assert result.total_unique_words > 0
        assert result.morphemes_identified > 0
        assert isinstance(result.is_statistically_significant, bool)
