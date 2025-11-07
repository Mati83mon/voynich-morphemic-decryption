"""FastAPI routes for Voynich analysis API."""

import logging
import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, status

from voynich_decryption import (
    MorphemicAnalyzer,
    StatisticalValidator,
    VoynichAnalysisPipeline,
)
from voynich_decryption.api.schemas import (
    AnalysisRequest,
    AnalysisResponse,
    AnalysisDetailResponse,
    WordDecompositionRequest,
    WordDecompositionResponse,
    HealthResponse,
    ErrorResponse,
    MorphemeSchema,
)
from voynich_decryption.__version__ import __version__

logger = logging.getLogger(__name__)

# Create API router
router = APIRouter()

# Global analyzer instance (initialized on first use)
_analyzer: Optional[MorphemicAnalyzer] = None
_validator: Optional[StatisticalValidator] = None


def get_analyzer() -> MorphemicAnalyzer:
    """Get or create morphemic analyzer instance."""
    global _analyzer
    if _analyzer is None:
        _analyzer = MorphemicAnalyzer(verbose=True)
        logger.info("Initialized MorphemicAnalyzer")
    return _analyzer


def get_validator() -> StatisticalValidator:
    """Get or create statistical validator instance."""
    global _validator
    if _validator is None:
        _validator = StatisticalValidator()
        logger.info("Initialized StatisticalValidator")
    return _validator


@router.get(
    "/",
    response_model=HealthResponse,
    summary="Root endpoint",
    description="Get API information",
)
async def root() -> HealthResponse:
    """Root endpoint returning API information."""
    return HealthResponse(
        status="online",
        version=__version__,
        timestamp=datetime.now(),
    )


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Check if API is running and healthy",
)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version=__version__,
        timestamp=datetime.now(),
    )


@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="Analyze vocabulary",
    description="Perform complete morphemic analysis on provided vocabulary",
)
async def analyze_vocabulary(request: AnalysisRequest) -> AnalysisResponse:
    """
    Perform morphemic analysis on vocabulary.

    This endpoint analyzes a collection of Voynich words, decomposing them
    into morphemes and performing statistical validation.
    """
    try:
        logger.info(f"Received analysis request for {len(request.vocabulary)} words")

        # Get analyzer instance
        analyzer = get_analyzer()
        validator = get_validator(significance_threshold=request.significance_threshold)

        # Load morpheme inventory if provided
        if request.morpheme_inventory:
            logger.info("Loading provided morpheme inventory")
            from voynich_decryption.models import Morpheme, MorphemeType

            for mid, mdata in request.morpheme_inventory.items():
                try:
                    morpheme = Morpheme(
                        glyph=mdata["glyph"],
                        morpheme_id=mid,
                        morpheme_type=MorphemeType(mdata.get("type", "unknown")),
                        frequency=mdata.get("frequency", 0),
                        confidence_score=mdata.get("confidence", 0.0),
                    )
                    analyzer.add_morpheme(morpheme)
                except Exception as e:
                    logger.warning(f"Skipping invalid morpheme {mid}: {e}")

        # Perform analysis
        logger.info("Starting morphemic analysis...")
        analysis = analyzer.analyze_vocabulary(request.vocabulary)

        # Perform validation
        logger.info("Performing statistical validation...")
        validation_results = validator.validate_morphemic_patterns(analysis)

        # Generate analysis ID
        analysis_id = str(uuid.uuid4())

        logger.info(f"Analysis complete: {analysis_id}")

        return AnalysisResponse(
            success=True,
            message="Analysis completed successfully",
            analysis_id=analysis_id,
            timestamp=datetime.now(),
            total_words_analyzed=analysis.total_words_analyzed,
            total_unique_words=analysis.total_unique_words,
            morphemes_identified=analysis.morphemes_identified,
            chi_square_statistic=float(analysis.chi_square_statistic),
            p_value=float(analysis.p_value),
            statistically_significant=analysis.is_statistically_significant,
            average_confidence=float(analysis.average_word_confidence),
        )

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid request: {str(e)}",
        )
    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}",
        )


@router.post(
    "/analyze/detailed",
    response_model=AnalysisDetailResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="Detailed analysis",
    description="Perform complete analysis with full detailed results",
)
async def analyze_vocabulary_detailed(
    request: AnalysisRequest,
) -> AnalysisDetailResponse:
    """
    Perform detailed morphemic analysis with full results.

    Returns complete analysis results including all morphemes and word analyses.
    """
    try:
        logger.info(
            f"Received detailed analysis request for {len(request.vocabulary)} words"
        )

        # Get analyzer instance
        analyzer = get_analyzer()
        validator = get_validator(significance_threshold=request.significance_threshold)

        # Load morpheme inventory if provided
        if request.morpheme_inventory:
            from voynich_decryption.models import Morpheme, MorphemeType

            for mid, mdata in request.morpheme_inventory.items():
                try:
                    morpheme = Morpheme(
                        glyph=mdata["glyph"],
                        morpheme_id=mid,
                        morpheme_type=MorphemeType(mdata.get("type", "unknown")),
                        frequency=mdata.get("frequency", 0),
                        confidence_score=mdata.get("confidence", 0.0),
                    )
                    analyzer.add_morpheme(morpheme)
                except Exception as e:
                    logger.warning(f"Skipping invalid morpheme {mid}: {e}")

        # Perform analysis
        analysis = analyzer.analyze_vocabulary(request.vocabulary)
        validation_results = validator.validate_morphemic_patterns(analysis)

        # Generate analysis ID
        analysis_id = str(uuid.uuid4())

        # Convert to response format
        morpheme_inventory = {
            mid: MorphemeSchema(
                morpheme_id=m.morpheme_id,
                glyph=m.glyph,
                type=m.morpheme_type.value,
                frequency=m.frequency,
                confidence=m.confidence_score,
                botanical_reference=m.botanical_reference,
                pharmaceutical_use=m.pharmaceutical_use,
            )
            for mid, m in analysis.morpheme_inventory.items()
        }

        word_analyses = [wa.to_dict() for wa in analysis.word_analyses]

        return AnalysisDetailResponse(
            success=True,
            message="Detailed analysis completed successfully",
            analysis_id=analysis_id,
            timestamp=datetime.now(),
            total_words_analyzed=analysis.total_words_analyzed,
            total_unique_words=analysis.total_unique_words,
            morphemes_identified=analysis.morphemes_identified,
            chi_square_statistic=float(analysis.chi_square_statistic),
            p_value=float(analysis.p_value),
            statistically_significant=analysis.is_statistically_significant,
            average_confidence=float(analysis.average_word_confidence),
            morpheme_inventory=morpheme_inventory,
            word_analyses=word_analyses,
            validation_results=validation_results,
        )

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid request: {str(e)}",
        )
    except Exception as e:
        logger.error(f"Detailed analysis failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}",
        )


@router.post(
    "/decompose",
    response_model=WordDecompositionResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="Decompose word",
    description="Decompose a single word into morphemes",
)
async def decompose_word(
    request: WordDecompositionRequest,
) -> WordDecompositionResponse:
    """
    Decompose a single word into its constituent morphemes.

    This endpoint analyzes a single word and returns its morphemic breakdown.
    """
    try:
        logger.info(f"Decomposing word: {request.word}")

        # Get analyzer instance
        analyzer = get_analyzer()

        # Generate word ID if not provided
        word_id = request.word_id or str(uuid.uuid4())

        # Decompose word
        analysis = analyzer.decompose_word(request.word, word_id)

        # Convert morphemes to schema format
        morphemes = [
            MorphemeSchema(
                morpheme_id=m.morpheme_id,
                glyph=m.glyph,
                type=m.morpheme_type.value,
                frequency=m.frequency,
                confidence=m.confidence_score,
                botanical_reference=m.botanical_reference,
                pharmaceutical_use=m.pharmaceutical_use,
            )
            for m in analysis.morphemes
        ]

        return WordDecompositionResponse(
            success=True,
            word=request.word,
            word_id=word_id,
            morphemes=morphemes,
            confidence=float(analysis.confidence),
            morpheme_count=analysis.morpheme_count,
        )

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid request: {str(e)}",
        )
    except Exception as e:
        logger.error(f"Word decomposition failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Decomposition failed: {str(e)}",
        )


@router.get(
    "/statistics",
    summary="Get analyzer statistics",
    description="Get current analyzer statistics and metrics",
)
async def get_statistics() -> dict:
    """Get analyzer statistics."""
    try:
        analyzer = get_analyzer()
        return analyzer.get_statistics()
    except Exception as e:
        logger.error(f"Failed to get statistics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get statistics: {str(e)}",
        )


@router.post(
    "/cache/clear",
    summary="Clear analyzer cache",
    description="Clear the word analysis cache",
)
async def clear_cache() -> dict:
    """Clear analyzer cache."""
    try:
        analyzer = get_analyzer()
        analyzer.clear_cache()
        return {"success": True, "message": "Cache cleared successfully"}
    except Exception as e:
        logger.error(f"Failed to clear cache: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear cache: {str(e)}",
        )
