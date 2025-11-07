"""Word analysis data model for Voynich manuscript."""

from dataclasses import dataclass, field
from typing import Optional

from voynich_decryption.models.morpheme import Morpheme


@dataclass
class WordAnalysis:
    """
    Complete morphemic analysis of a single word.

    This class represents the result of decomposing a Voynich word into
    its constituent morphemes along with associated metadata.

    Attributes:
        word_glyph: The original word glyph/text
        word_id: Unique identifier for this word
        morphemes: List of identified morphemes in the word
        total_frequency: Total frequency of all morphemes combined
        statistical_significance: Statistical significance of the analysis
        potential_meaning: Hypothesized meaning based on morpheme analysis
        confidence: Overall confidence in the analysis (0.0-1.0)
        verification_status: Status of verification (unverified, pending, verified)
    """

    word_glyph: str
    word_id: str
    morphemes: list[Morpheme] = field(default_factory=list)
    total_frequency: int = 0
    statistical_significance: float = 0.0
    potential_meaning: Optional[str] = None
    confidence: float = 0.0
    verification_status: str = "unverified"

    def __post_init__(self) -> None:
        """Validate word analysis data after initialization."""
        if not self.word_glyph:
            raise ValueError("Word glyph cannot be empty")
        if not self.word_id:
            raise ValueError("Word ID cannot be empty")
        if not 0 <= self.confidence <= 1:
            raise ValueError(f"Confidence must be between 0 and 1, got {self.confidence}")
        if self.verification_status not in ["unverified", "pending", "verified"]:
            raise ValueError(
                f"Invalid verification status: {self.verification_status}. "
                "Must be one of: unverified, pending, verified"
            )

    @property
    def morpheme_count(self) -> int:
        """Return the number of morphemes in this word."""
        return len(self.morphemes)

    @property
    def is_verified(self) -> bool:
        """Check if this word analysis has been verified."""
        return self.verification_status == "verified"

    @property
    def average_morpheme_confidence(self) -> float:
        """
        Calculate average confidence score across all morphemes.

        Returns:
            Average confidence score, or 0.0 if no morphemes
        """
        if not self.morphemes:
            return 0.0
        return sum(m.confidence_score for m in self.morphemes) / len(self.morphemes)

    def __str__(self) -> str:
        """Return string representation of word analysis."""
        return (
            f"WordAnalysis({self.word_id}: '{self.word_glyph}', "
            f"{self.morpheme_count} morphemes, confidence={self.confidence:.2f})"
        )

    def __repr__(self) -> str:
        """Return detailed representation of word analysis."""
        return (
            f"WordAnalysis(word_glyph='{self.word_glyph}', word_id='{self.word_id}', "
            f"morphemes={len(self.morphemes)}, total_frequency={self.total_frequency}, "
            f"confidence={self.confidence:.2f}, verification_status='{self.verification_status}')"
        )

    def to_dict(self) -> dict[str, any]:
        """
        Convert word analysis to dictionary format.

        Returns:
            Dictionary representation of the word analysis
        """
        return {
            "word_glyph": self.word_glyph,
            "word_id": self.word_id,
            "morphemes": [m.to_dict() for m in self.morphemes],
            "morpheme_count": self.morpheme_count,
            "total_frequency": self.total_frequency,
            "statistical_significance": float(self.statistical_significance),
            "potential_meaning": self.potential_meaning,
            "confidence": float(self.confidence),
            "average_morpheme_confidence": float(self.average_morpheme_confidence),
            "verification_status": self.verification_status,
            "is_verified": self.is_verified,
        }

    @classmethod
    def from_dict(cls, data: dict[str, any]) -> "WordAnalysis":
        """
        Create WordAnalysis instance from dictionary.

        Args:
            data: Dictionary containing word analysis data

        Returns:
            WordAnalysis instance

        Raises:
            ValueError: If required fields are missing
        """
        morphemes = [
            Morpheme.from_dict(m) if isinstance(m, dict) else m
            for m in data.get("morphemes", [])
        ]

        return cls(
            word_glyph=data["word_glyph"],
            word_id=data["word_id"],
            morphemes=morphemes,
            total_frequency=data.get("total_frequency", 0),
            statistical_significance=data.get("statistical_significance", 0.0),
            potential_meaning=data.get("potential_meaning"),
            confidence=data.get("confidence", 0.0),
            verification_status=data.get("verification_status", "unverified"),
        )
