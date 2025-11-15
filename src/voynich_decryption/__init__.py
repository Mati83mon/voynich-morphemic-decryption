"""
Voynich Morphemic Decryption - Advanced morphemic analysis of Voynich Manuscript.

This package provides tools for analyzing and decrypting the Voynich manuscript
through morphemic decomposition, statistical validation, and pattern recognition.
"""

from voynich_decryption.__version__ import (
    __author__,
    __email__,
    __license__,
    __version__,
)
from voynich_decryption.core import MorphemicAnalyzer, StatisticalValidator
from voynich_decryption.models import (
    AnalysisResult,
    Morpheme,
    MorphemeType,
    WordAnalysis,
)
from voynich_decryption.pipelines import (
    ReportGenerator,
    VoynichAnalysisPipeline,
)

__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    # Core components
    "MorphemicAnalyzer",
    "StatisticalValidator",
    # Models
    "Morpheme",
    "MorphemeType",
    "WordAnalysis",
    "AnalysisResult",
    # Pipelines
    "VoynichAnalysisPipeline",
    "ReportGenerator",
]
