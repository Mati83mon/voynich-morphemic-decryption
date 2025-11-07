"""Data models for Voynich Morphemic Decryption."""

from voynich_decryption.models.morpheme import Morpheme, MorphemeType
from voynich_decryption.models.word_analysis import WordAnalysis
from voynich_decryption.models.analysis_result import AnalysisResult

__all__ = [
    "Morpheme",
    "MorphemeType",
    "WordAnalysis",
    "AnalysisResult",
]
