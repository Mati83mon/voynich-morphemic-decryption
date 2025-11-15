"""Advanced morphemic decomposition engine for Voynich manuscript."""

import json
import logging
from pathlib import Path

import numpy as np
from scipy.stats import chi2

from voynich_decryption.models import (
    AnalysisResult,
    Morpheme,
    MorphemeType,
    WordAnalysis,
)

logger = logging.getLogger(__name__)


class MorphemicAnalyzer:
    """
    Advanced morphemic decomposition engine.

    This class handles the analysis of Voynich manuscript text by decomposing
    words into their constituent morphemes and performing statistical validation.

    Attributes:
        morpheme_inventory: Dictionary of known morphemes indexed by morpheme_id
        word_cache: Cache of analyzed words to avoid redundant processing
        verbose: Enable verbose logging output
    """

    def __init__(
        self,
        vocabulary_file: str | None = None,
        verbose: bool = True,
    ) -> None:
        """
        Initialize the morphemic analyzer.

        Args:
            vocabulary_file: Optional path to JSON file containing morpheme vocabulary
            verbose: Enable verbose logging output
        """
        self.verbose = verbose
        self.morpheme_inventory: dict[str, Morpheme] = {}
        self.word_cache: dict[str, WordAnalysis] = {}

        if vocabulary_file:
            self.load_vocabulary(vocabulary_file)

        if self.verbose:
            logger.info("MorphemicAnalyzer initialized successfully")

    def load_vocabulary(self, filepath: str) -> None:
        """
        Load predefined morpheme vocabulary from JSON file.

        Args:
            filepath: Path to vocabulary JSON file

        Raises:
            FileNotFoundError: If vocabulary file doesn't exist
            ValueError: If vocabulary file has invalid format
        """
        try:
            vocab_path = Path(filepath)
            if not vocab_path.exists():
                raise FileNotFoundError(f"Vocabulary file not found: {filepath}")

            with open(vocab_path, encoding="utf-8") as f:
                vocab_data = json.load(f)

            if not isinstance(vocab_data, dict):
                raise ValueError("Vocabulary file must contain a JSON object")

            for morpheme_id, data in vocab_data.items():
                if not isinstance(data, dict):
                    logger.warning(f"Skipping invalid morpheme data for {morpheme_id}")
                    continue

                try:
                    morpheme = Morpheme(
                        glyph=data.get("glyph", ""),
                        morpheme_id=morpheme_id,
                        morpheme_type=MorphemeType(data.get("type", "unknown")),
                        frequency=data.get("frequency", 0),
                        confidence_score=data.get("confidence", 0.0),
                        related_morphemes=data.get("related_morphemes", []),
                        botanical_reference=data.get("botanical_ref"),
                        pharmaceutical_use=data.get("pharmaceutical_use"),
                        historical_notes=data.get("historical_notes"),
                    )
                    self.morpheme_inventory[morpheme_id] = morpheme
                except (ValueError, KeyError) as e:
                    logger.warning(f"Error loading morpheme {morpheme_id}: {e}")
                    continue

            if self.verbose:
                logger.info(f"Loaded {len(self.morpheme_inventory)} morphemes from {filepath}")

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in vocabulary file: {e}")
            raise ValueError(f"Invalid JSON in vocabulary file: {e}") from e
        except Exception as e:
            logger.error(f"Failed to load vocabulary: {e}")
            raise

    def add_morpheme(self, morpheme: Morpheme) -> None:
        """
        Add a morpheme to the inventory.

        Args:
            morpheme: Morpheme instance to add

        Raises:
            ValueError: If morpheme with same ID already exists
        """
        if morpheme.morpheme_id in self.morpheme_inventory:
            raise ValueError(f"Morpheme with ID '{morpheme.morpheme_id}' already exists")
        self.morpheme_inventory[morpheme.morpheme_id] = morpheme
        logger.debug(f"Added morpheme: {morpheme.morpheme_id}")

    def decompose_word(self, word_glyph: str, word_id: str) -> WordAnalysis:
        """
        Decompose a word into morphemic components.

        Uses a greedy algorithm to find the longest matching morphemes first.

        Args:
            word_glyph: The word to analyze
            word_id: Unique identifier for the word

        Returns:
            WordAnalysis containing decomposition results

        Raises:
            ValueError: If word_glyph or word_id is empty
        """
        if not word_glyph:
            raise ValueError("Word glyph cannot be empty")
        if not word_id:
            raise ValueError("Word ID cannot be empty")

        # Check cache first
        if word_id in self.word_cache:
            logger.debug(f"Returning cached analysis for word: {word_id}")
            return self.word_cache[word_id]

        # Perform morpheme decomposition
        morphemes = self._find_morpheme_sequences(word_glyph)

        # Calculate statistics
        total_frequency = sum(m.frequency for m in morphemes)
        confidence = float(np.mean([m.confidence_score for m in morphemes])) if morphemes else 0.0

        analysis = WordAnalysis(
            word_glyph=word_glyph,
            word_id=word_id,
            morphemes=morphemes,
            total_frequency=total_frequency,
            confidence=confidence,
        )

        # Cache the result
        self.word_cache[word_id] = analysis

        if self.verbose:
            logger.debug(
                f"Decomposed word '{word_id}': {len(morphemes)} morphemes, "
                f"confidence={confidence:.2f}"
            )

        return analysis

    def _find_morpheme_sequences(self, word: str) -> list[Morpheme]:
        """
        Find morpheme sequences within a word using greedy algorithm.

        The algorithm tries to match the longest possible morphemes first,
        falling back to shorter matches when necessary.

        Args:
            word: Word to decompose

        Returns:
            List of identified morphemes in sequence
        """
        morphemes: list[Morpheme] = []
        remaining = word
        position = 0

        while remaining:
            matched = False

            # Try longest matches first (greedy approach)
            for length in range(len(remaining), 0, -1):
                segment = remaining[:length]

                # Search for matching morpheme in inventory
                for morpheme in self.morpheme_inventory.values():
                    if morpheme.glyph == segment:
                        morphemes.append(morpheme)
                        remaining = remaining[length:]
                        position += length
                        matched = True
                        break

                if matched:
                    break

            if not matched:
                # Create unknown morpheme for unmatched character
                unknown = Morpheme(
                    glyph=remaining[0],
                    morpheme_id=f"unknown_{position}_{id(remaining)}",
                    morpheme_type=MorphemeType.UNKNOWN,
                    confidence_score=0.0,
                )
                morphemes.append(unknown)
                remaining = remaining[1:]
                position += 1
                logger.debug(f"Unknown morpheme at position {position}: '{unknown.glyph}'")

        return morphemes

    def analyze_vocabulary(self, vocabulary: dict[str, str]) -> AnalysisResult:
        """
        Perform complete morphemic analysis on vocabulary.

        Args:
            vocabulary: Dictionary mapping word_id to word_glyph

        Returns:
            Comprehensive analysis results with statistical validation

        Raises:
            ValueError: If vocabulary is empty or invalid
        """
        if not vocabulary:
            raise ValueError("Vocabulary cannot be empty")

        if self.verbose:
            logger.info(f"Starting analysis of {len(vocabulary)} words...")

        word_analyses: list[WordAnalysis] = []

        for word_id, word_glyph in vocabulary.items():
            try:
                analysis = self.decompose_word(word_glyph, word_id)
                word_analyses.append(analysis)
            except Exception as e:
                logger.error(f"Error analyzing word {word_id}: {e}")
                continue

        # Perform statistical validation
        chi_square, p_value = self._perform_chi_square_test(word_analyses)

        result = AnalysisResult(
            total_words_analyzed=len(vocabulary),
            total_unique_words=len(set(vocabulary.values())),
            morphemes_identified=len(self.morpheme_inventory),
            chi_square_statistic=chi_square,
            p_value=p_value,
            morpheme_inventory=self.morpheme_inventory,
            word_analyses=word_analyses,
            metadata={
                "analyzer_version": "1.0.0",
                "vocabulary_size": len(vocabulary),
            },
        )

        if self.verbose:
            logger.info(f"Analysis complete: χ² = {chi_square:.4f}, p = {p_value:.6f}")
            logger.info(f"Statistical significance: {result.is_statistically_significant}")

        return result

    def _perform_chi_square_test(self, word_analyses: list[WordAnalysis]) -> tuple[float, float]:
        """
        Perform chi-square test for non-random morpheme distribution.

        Tests whether the observed morpheme frequency distribution differs
        significantly from a uniform distribution (null hypothesis).

        Args:
            word_analyses: List of word analysis results

        Returns:
            Tuple of (chi_square_statistic, p_value)
        """
        if not word_analyses:
            logger.warning("No word analyses provided for chi-square test")
            return 0.0, 1.0

        # Build frequency contingency table
        morpheme_frequencies: dict[str, int] = {}
        for analysis in word_analyses:
            for morpheme in analysis.morphemes:
                morpheme_frequencies[morpheme.morpheme_id] = (
                    morpheme_frequencies.get(morpheme.morpheme_id, 0) + 1
                )

        if not morpheme_frequencies:
            logger.warning("No morphemes found in word analyses")
            return 0.0, 1.0

        # Calculate chi-square statistic
        observed_frequencies = np.array(list(morpheme_frequencies.values()))
        total = observed_frequencies.sum()
        expected_freq = total / len(morpheme_frequencies)

        # Chi-square calculation: Σ((O - E)² / E)
        chi_square_stat = float(np.sum((observed_frequencies - expected_freq) ** 2 / expected_freq))

        # Degrees of freedom
        df = len(morpheme_frequencies) - 1

        # Calculate p-value from chi-square distribution
        if df > 0:
            p_value = float(1 - chi2.cdf(chi_square_stat, df))
        else:
            p_value = 1.0

        logger.debug(f"Chi-square test: χ² = {chi_square_stat:.4f}, df = {df}, p = {p_value:.6f}")

        return chi_square_stat, p_value

    def clear_cache(self) -> None:
        """Clear the word analysis cache."""
        self.word_cache.clear()
        logger.debug("Word analysis cache cleared")

    def get_statistics(self) -> dict[str, any]:
        """
        Get analyzer statistics.

        Returns:
            Dictionary containing analyzer statistics
        """
        return {
            "morphemes_in_inventory": len(self.morpheme_inventory),
            "cached_word_analyses": len(self.word_cache),
            "morpheme_types": {
                mtype.value: sum(
                    1 for m in self.morpheme_inventory.values() if m.morpheme_type == mtype
                )
                for mtype in MorphemeType
            },
        }
