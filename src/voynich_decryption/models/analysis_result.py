"""Analysis result data model for Voynich manuscript."""

from dataclasses import dataclass, field

from voynich_decryption.models.morpheme import Morpheme
from voynich_decryption.models.word_analysis import WordAnalysis


@dataclass
class AnalysisResult:
    """
    Comprehensive analysis results for Voynich manuscript.

    This class contains the complete output of a morphemic analysis,
    including statistical validation and all identified patterns.

    Attributes:
        total_words_analyzed: Total number of words processed
        total_unique_words: Number of unique word forms
        morphemes_identified: Number of distinct morphemes identified
        chi_square_statistic: Chi-square test statistic
        p_value: P-value from statistical test
        statistical_significance_threshold: Threshold for significance (default 0.05)
        morpheme_inventory: Dictionary of all identified morphemes
        word_analyses: List of all word analysis results
        metadata: Additional metadata about the analysis
    """

    total_words_analyzed: int
    total_unique_words: int
    morphemes_identified: int
    chi_square_statistic: float
    p_value: float
    statistical_significance_threshold: float = 0.05
    morpheme_inventory: dict[str, Morpheme] = field(default_factory=dict)
    word_analyses: list[WordAnalysis] = field(default_factory=list)
    metadata: dict[str, any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate analysis result data after initialization."""
        if self.total_words_analyzed < 0:
            raise ValueError("Total words analyzed must be non-negative")
        if self.total_unique_words < 0:
            raise ValueError("Total unique words must be non-negative")
        if self.morphemes_identified < 0:
            raise ValueError("Morphemes identified must be non-negative")
        if self.total_unique_words > self.total_words_analyzed:
            raise ValueError("Unique words cannot exceed total words")

    @property
    def is_statistically_significant(self) -> bool:
        """
        Check if results are statistically significant.

        Returns:
            True if p-value is below the significance threshold
        """
        return bool(self.p_value < self.statistical_significance_threshold)

    @property
    def verified_words_count(self) -> int:
        """Count how many word analyses have been verified."""
        return sum(1 for wa in self.word_analyses if wa.is_verified)

    @property
    def average_word_confidence(self) -> float:
        """
        Calculate average confidence across all word analyses.

        Returns:
            Average confidence score, or 0.0 if no analyses
        """
        if not self.word_analyses:
            return 0.0
        return sum(wa.confidence for wa in self.word_analyses) / len(self.word_analyses)

    @property
    def high_confidence_words(self) -> list[WordAnalysis]:
        """
        Get list of word analyses with high confidence (>= 0.7).

        Returns:
            List of high-confidence word analyses
        """
        return [wa for wa in self.word_analyses if wa.confidence >= 0.7]

    @property
    def morpheme_frequency_distribution(self) -> dict[str, int]:
        """
        Get frequency distribution of all morphemes.

        Returns:
            Dictionary mapping morpheme IDs to frequencies
        """
        return {mid: m.frequency for mid, m in self.morpheme_inventory.items()}

    def __str__(self) -> str:
        """Return string representation of analysis results."""
        return (
            f"AnalysisResult(words={self.total_words_analyzed}, "
            f"morphemes={self.morphemes_identified}, "
            f"χ²={self.chi_square_statistic:.2f}, p={self.p_value:.4f}, "
            f"significant={self.is_statistically_significant})"
        )

    def __repr__(self) -> str:
        """Return detailed representation of analysis results."""
        return (
            f"AnalysisResult(total_words_analyzed={self.total_words_analyzed}, "
            f"total_unique_words={self.total_unique_words}, "
            f"morphemes_identified={self.morphemes_identified}, "
            f"chi_square={self.chi_square_statistic:.4f}, "
            f"p_value={self.p_value:.6f}, "
            f"significant={self.is_statistically_significant})"
        )

    def to_dict(self) -> dict[str, any]:
        """
        Convert analysis results to dictionary format.

        Returns:
            Dictionary representation of the results
        """
        return {
            "summary": {
                "total_words_analyzed": self.total_words_analyzed,
                "total_unique_words": self.total_unique_words,
                "morphemes_identified": self.morphemes_identified,
                "verified_words_count": self.verified_words_count,
                "average_word_confidence": float(self.average_word_confidence),
                "high_confidence_words_count": len(self.high_confidence_words),
            },
            "statistical_results": {
                "chi_square_statistic": float(self.chi_square_statistic),
                "p_value": float(self.p_value),
                "threshold": float(self.statistical_significance_threshold),
                "statistically_significant": self.is_statistically_significant,
            },
            "morpheme_inventory": {mid: m.to_dict() for mid, m in self.morpheme_inventory.items()},
            "word_analyses": [wa.to_dict() for wa in self.word_analyses],
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, any]) -> "AnalysisResult":
        """
        Create AnalysisResult instance from dictionary.

        Args:
            data: Dictionary containing analysis results data

        Returns:
            AnalysisResult instance

        Raises:
            ValueError: If required fields are missing
        """
        summary = data.get("summary", {})
        stats = data.get("statistical_results", {})

        # Reconstruct morpheme inventory
        morpheme_inventory = {}
        for mid, mdata in data.get("morpheme_inventory", {}).items():
            morpheme_inventory[mid] = (
                Morpheme.from_dict(mdata) if isinstance(mdata, dict) else mdata
            )

        # Reconstruct word analyses
        word_analyses = [
            WordAnalysis.from_dict(wa) if isinstance(wa, dict) else wa
            for wa in data.get("word_analyses", [])
        ]

        return cls(
            total_words_analyzed=summary.get("total_words_analyzed", 0),
            total_unique_words=summary.get("total_unique_words", 0),
            morphemes_identified=summary.get("morphemes_identified", 0),
            chi_square_statistic=stats.get("chi_square_statistic", 0.0),
            p_value=stats.get("p_value", 1.0),
            statistical_significance_threshold=stats.get("threshold", 0.05),
            morpheme_inventory=morpheme_inventory,
            word_analyses=word_analyses,
            metadata=data.get("metadata", {}),
        )

    def get_summary_report(self) -> str:
        """
        Generate a human-readable summary report.

        Returns:
            Formatted summary report string
        """
        report_lines = [
            "=" * 70,
            "VOYNICH MANUSCRIPT MORPHEMIC ANALYSIS RESULTS",
            "=" * 70,
            "",
            f"Total Words Analyzed:      {self.total_words_analyzed:,}",
            f"Unique Words:              {self.total_unique_words:,}",
            f"Morphemes Identified:      {self.morphemes_identified:,}",
            f"Verified Words:            {self.verified_words_count:,}",
            "",
            "Statistical Analysis:",
            f"  Chi-Square Statistic:    {self.chi_square_statistic:.4f}",
            f"  P-Value:                 {self.p_value:.6f}",
            f"  Significance Threshold:  {self.statistical_significance_threshold}",
            f"  Statistically Significant: {'YES' if self.is_statistically_significant else 'NO'}",
            "",
            "Confidence Metrics:",
            f"  Average Word Confidence: {self.average_word_confidence:.2%}",
            f"  High Confidence Words:   {len(self.high_confidence_words):,}",
            "",
            "=" * 70,
        ]
        return "\n".join(report_lines)
