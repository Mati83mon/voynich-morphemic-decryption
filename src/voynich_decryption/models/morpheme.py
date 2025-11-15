"""Morpheme data models for Voynich manuscript analysis."""

from dataclasses import dataclass, field
from enum import Enum


class MorphemeType(Enum):
    """Classification of morpheme types in Voynich text."""

    ROOT = "root"
    PREFIX = "prefix"
    SUFFIX = "suffix"
    INFIX = "infix"
    COMPOUND = "compound"
    UNKNOWN = "unknown"


@dataclass
class Morpheme:
    """
    Represents a single morpheme unit in Voynich manuscript.

    A morpheme is the smallest meaningful unit in the text analysis.

    Attributes:
        glyph: The actual glyph or character sequence
        morpheme_id: Unique identifier for this morpheme
        morpheme_type: Type classification of the morpheme
        frequency: Number of occurrences in the corpus
        confidence_score: Confidence level of identification (0.0-1.0)
        related_morphemes: List of related morpheme IDs
        botanical_reference: Reference to botanical context (if any)
        pharmaceutical_use: Reference to pharmaceutical context (if any)
        historical_notes: Additional historical context
    """

    glyph: str
    morpheme_id: str
    morpheme_type: MorphemeType
    frequency: int = 0
    confidence_score: float = 0.0
    related_morphemes: list[str] = field(default_factory=list)
    botanical_reference: str | None = None
    pharmaceutical_use: str | None = None
    historical_notes: str | None = None

    def __post_init__(self) -> None:
        """Validate morpheme data after initialization."""
        if not 0 <= self.confidence_score <= 1:
            raise ValueError(
                f"Confidence score must be between 0 and 1, got {self.confidence_score}"
            )
        if self.frequency < 0:
            raise ValueError(f"Frequency must be non-negative, got {self.frequency}")
        if not self.glyph:
            raise ValueError("Glyph cannot be empty")
        if not self.morpheme_id:
            raise ValueError("Morpheme ID cannot be empty")

    def __str__(self) -> str:
        """Return string representation of morpheme."""
        return f"Morpheme({self.morpheme_id}: {self.glyph}, type={self.morpheme_type.value})"

    def __repr__(self) -> str:
        """Return detailed representation of morpheme."""
        return (
            f"Morpheme(glyph='{self.glyph}', morpheme_id='{self.morpheme_id}', "
            f"morpheme_type={self.morpheme_type}, frequency={self.frequency}, "
            f"confidence_score={self.confidence_score:.2f})"
        )

    def to_dict(self) -> dict[str, any]:
        """
        Convert morpheme to dictionary format.

        Returns:
            Dictionary representation of the morpheme
        """
        return {
            "glyph": self.glyph,
            "morpheme_id": self.morpheme_id,
            "type": self.morpheme_type.value,
            "frequency": self.frequency,
            "confidence": float(self.confidence_score),
            "related_morphemes": self.related_morphemes,
            "botanical_reference": self.botanical_reference,
            "pharmaceutical_use": self.pharmaceutical_use,
            "historical_notes": self.historical_notes,
        }

    @classmethod
    def from_dict(cls, data: dict[str, any]) -> "Morpheme":
        """
        Create Morpheme instance from dictionary.

        Args:
            data: Dictionary containing morpheme data

        Returns:
            Morpheme instance

        Raises:
            ValueError: If required fields are missing
        """
        return cls(
            glyph=data["glyph"],
            morpheme_id=data["morpheme_id"],
            morpheme_type=MorphemeType(data.get("type", "unknown")),
            frequency=data.get("frequency", 0),
            confidence_score=data.get("confidence", 0.0),
            related_morphemes=data.get("related_morphemes", []),
            botanical_reference=data.get("botanical_reference"),
            pharmaceutical_use=data.get("pharmaceutical_use"),
            historical_notes=data.get("historical_notes"),
        )
