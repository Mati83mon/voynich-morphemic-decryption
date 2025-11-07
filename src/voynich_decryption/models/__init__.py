"""Data models for Voynich Morphemic Decryption."""

from voynich_decryption.models.analysis_result import AnalysisResult
from voynich_decryption.models.morpheme import Morpheme, MorphemeType
from voynich_decryption.models.word_analysis import WordAnalysis

__all__ = [
    "Morpheme",
    "MorphemeType",
    "WordAnalysis",
    "AnalysisResult",
]
