"""
Voynich Morphemic Decryption - Advanced morphemic analysis of Voynich Manuscript.

This package provides tools for analyzing and decrypting the Voynich manuscript
through morphemic decomposition, statistical validation, and pattern recognition.
"""

from voynich_decryption.__version__ import (
    __version__,
    __author__,
    __email__,
    __license__,
)

from voynich_decryption.core import MorphemicAnalyzer, StatisticalValidator
from voynich_decryption.models import (
    Morpheme,
    MorphemeType,
    WordAnalysis,
    AnalysisResult,
)
from voynich_decryption.pipelines import (
    VoynichAnalysisPipeline,
    ReportGenerator,
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
